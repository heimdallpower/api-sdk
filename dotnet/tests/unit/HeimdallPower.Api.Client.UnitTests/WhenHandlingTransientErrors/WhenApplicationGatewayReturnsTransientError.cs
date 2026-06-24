using System.Net;
using HeimdallPower.Api.Client.UnitTests.WhenHandlingTransientErrors.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingTransientErrors;

/// <summary>
/// Verifies that <see cref="HeimdallApiHttpClient"/> retries automatically when the
/// Application Gateway returns a transient error (500 / 502 / 503 / 504), including
/// the case where the response body is an HTML page instead of JSON.
/// Also verifies that the client does NOT retry on non-transient errors (400, 401, 404).
/// </summary>
[Trait("Category", "Unit")]
public class WhenApplicationGatewayReturnsTransientError
{
    // -----------------------------------------------------------------------
    // Helpers
    // -----------------------------------------------------------------------

    /// <summary>
    /// Simple DTO used as the expected deserialization target.
    /// Matches {"data":{"value":"ok"}} wrapped in ApiResponse.
    /// </summary>
    private record SimpleData(string Value);

    private const string OkJson = """{"value":"ok"}""";

    // -----------------------------------------------------------------------
    // 504 Gateway Timeout with HTML body — the original customer bug
    // -----------------------------------------------------------------------

    [Fact(DisplayName = "504 with HTML body: retries 3 times before giving up")]
    public async Task GatewayTimeout_WithHtmlBody_RetriesThreeTimes()
    {
        var handler = new FakeHttpMessageHandler(
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.GatewayTimeout),
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.GatewayTimeout),
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.GatewayTimeout),
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.GatewayTimeout)  // exhausts retries
        );
        var client = HeimdallApiHttpClientFactory.Create(handler);

        await Assert.ThrowsAsync<HeimdallApiException>(() => client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        // 1 initial attempt + 3 retries = 4 total HTTP calls
        Assert.Equal(4, handler.CallCount);
    }

    [Fact(DisplayName = "504 with HTML body: final exception carries GatewayTimeout status code")]
    public async Task GatewayTimeout_WithHtmlBody_ThrowsHeimdallApiExceptionWithCorrectStatusCode()
    {
        var client = HeimdallApiHttpClientFactory.CreateWithFixedResponse(
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.GatewayTimeout));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        Assert.Equal(HttpStatusCode.GatewayTimeout, ex.StatusCode);
    }

    [Fact(DisplayName = "504 with HTML body: does NOT throw JsonException (original customer crash)")]
    public async Task GatewayTimeout_WithHtmlBody_DoesNotThrowJsonException()
    {
        var client = HeimdallApiHttpClientFactory.CreateWithFixedResponse(
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.GatewayTimeout));

        var exception = await Record.ExceptionAsync(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        // Must not be a JsonException — the old code threw this
        Assert.IsNotType<System.Text.Json.JsonException>(exception);
        // Must be a clean HeimdallApiException instead
        Assert.IsType<HeimdallApiException>(exception);
    }

    [Fact(DisplayName = "504 with HTML body: succeeds on the second attempt (recover after one transient failure)")]
    public async Task GatewayTimeout_WithHtmlBody_SucceedsAfterOneRetry()
    {
        var handler = new FakeHttpMessageHandler(
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.GatewayTimeout),
            FakeHttpMessageHandler.OkApiResponse(OkJson)
        );
        var client = HeimdallApiHttpClientFactory.Create(handler);

        var result = await client.GetAsync<ApiResponse<SimpleData>>("/fake");

        Assert.Equal("ok", result.Data.Value);
        Assert.Equal(2, handler.CallCount);
    }

    // -----------------------------------------------------------------------
    // 500 Internal Server Error with HTML body
    // -----------------------------------------------------------------------

    [Fact(DisplayName = "500 with HTML body: does NOT throw JsonException (original customer crash)")]
    public async Task InternalServerError_WithHtmlBody_DoesNotThrowJsonException()
    {
        var client = HeimdallApiHttpClientFactory.CreateWithFixedResponse(
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.InternalServerError));

        var exception = await Record.ExceptionAsync(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        Assert.IsNotType<System.Text.Json.JsonException>(exception);
        Assert.IsType<HeimdallApiException>(exception);
        Assert.Equal(HttpStatusCode.InternalServerError, ((HeimdallApiException)exception!).StatusCode);
    }

    [Fact(DisplayName = "500 with HTML body: retries 3 times before giving up")]
    public async Task InternalServerError_WithHtmlBody_RetriesThreeTimes()
    {
        var handler = new FakeHttpMessageHandler(
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.InternalServerError),
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.InternalServerError),
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.InternalServerError),
            FakeHttpMessageHandler.HtmlResponse(HttpStatusCode.InternalServerError)
        );
        var client = HeimdallApiHttpClientFactory.Create(handler);

        await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        Assert.Equal(4, handler.CallCount);
    }

    [Fact(DisplayName = "500 with JSON ProblemDetails body: exception message comes from ProblemDetails")]
    public async Task InternalServerError_WithJsonProblemDetails_ExceptionMessageIsFromProblemDetails()
    {
        var problemJson = """{"title":"Internal Error","detail":"Something went wrong on the server.","status":500}""";
        var response = new HttpResponseMessage(HttpStatusCode.InternalServerError)
        {
            Content = new System.Net.Http.StringContent(problemJson, System.Text.Encoding.UTF8, "application/json")
        };
        var handler = new FakeHttpMessageHandler(response, response, response, response);
        var client = HeimdallApiHttpClientFactory.Create(handler);

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        Assert.Contains("Something went wrong on the server.", ex.Message);
    }

    // -----------------------------------------------------------------------
    // [Theory] — all four transient status codes behave the same way
    // -----------------------------------------------------------------------

    [Theory(DisplayName = "Transient status code: retries 3 times and throws HeimdallApiException")]
    [InlineData(HttpStatusCode.InternalServerError)]
    [InlineData(HttpStatusCode.BadGateway)]
    [InlineData(HttpStatusCode.ServiceUnavailable)]
    [InlineData(HttpStatusCode.GatewayTimeout)]
    public async Task TransientStatusCode_WithHtmlBody_RetriesAndThrows(HttpStatusCode statusCode)
    {
        var handler = new FakeHttpMessageHandler(
            FakeHttpMessageHandler.HtmlResponse(statusCode),
            FakeHttpMessageHandler.HtmlResponse(statusCode),
            FakeHttpMessageHandler.HtmlResponse(statusCode),
            FakeHttpMessageHandler.HtmlResponse(statusCode)
        );
        var client = HeimdallApiHttpClientFactory.Create(handler);

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        Assert.Equal(statusCode, ex.StatusCode);
        Assert.Equal(4, handler.CallCount); // 1 initial + 3 retries
    }

    [Theory(DisplayName = "Transient status code: recovers after first failure")]
    [InlineData(HttpStatusCode.InternalServerError)]
    [InlineData(HttpStatusCode.BadGateway)]
    [InlineData(HttpStatusCode.ServiceUnavailable)]
    [InlineData(HttpStatusCode.GatewayTimeout)]
    public async Task TransientStatusCode_SucceedsAfterOneRetry(HttpStatusCode statusCode)
    {
        var handler = new FakeHttpMessageHandler(
            FakeHttpMessageHandler.HtmlResponse(statusCode),
            FakeHttpMessageHandler.OkApiResponse(OkJson)
        );
        var client = HeimdallApiHttpClientFactory.Create(handler);

        var result = await client.GetAsync<ApiResponse<SimpleData>>("/fake");

        Assert.Equal("ok", result.Data.Value);
        Assert.Equal(2, handler.CallCount);
    }

    // -----------------------------------------------------------------------
    // [Theory] — non-transient status codes must NOT be retried
    // -----------------------------------------------------------------------

    // 401 throws UnauthorizedAccessException (not HeimdallApiException) — it's intentionally excluded here
    // and covered by the dedicated test below.
    [Theory(DisplayName = "Non-transient status code: throws immediately without any retry")]
    [InlineData(HttpStatusCode.BadRequest)]
    [InlineData(HttpStatusCode.Forbidden)]
    [InlineData(HttpStatusCode.NotFound)]
    public async Task NonTransientStatusCode_ThrowsImmediatelyWithoutRetry(HttpStatusCode statusCode)
    {
        var handler = new FakeHttpMessageHandler(
            FakeHttpMessageHandler.HtmlResponse(statusCode)
        );
        var client = HeimdallApiHttpClientFactory.Create(handler);

        await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        // Only 1 HTTP call — no retry
        Assert.Equal(1, handler.CallCount);
    }

    [Theory(DisplayName = "Non-transient status code: exception carries the correct status code")]
    [InlineData(HttpStatusCode.BadRequest)]
    [InlineData(HttpStatusCode.Forbidden)]
    [InlineData(HttpStatusCode.NotFound)]
    public async Task NonTransientStatusCode_ExceptionHasCorrectStatusCode(HttpStatusCode statusCode)
    {
        var client = HeimdallApiHttpClientFactory.CreateWithFixedResponse(
            FakeHttpMessageHandler.HtmlResponse(statusCode));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        Assert.Equal(statusCode, ex.StatusCode);
    }

    // -----------------------------------------------------------------------
    // 401 Unauthorized — triggers auth-refresh, not a generic retry
    // -----------------------------------------------------------------------

    [Fact(DisplayName = "401 Unauthorized: triggers one token-refresh retry, then throws")]
    public async Task Unauthorized_TriggersAuthRefreshOnce_ThenThrows()
    {
        // Both attempts return 401 — the auth retry should happen once,
        // giving 2 total HTTP calls before giving up.
        var handler = new FakeHttpMessageHandler(
            new HttpResponseMessage(HttpStatusCode.Unauthorized),
            new HttpResponseMessage(HttpStatusCode.Unauthorized)
        );
        var client = HeimdallApiHttpClientFactory.Create(handler);

        await Assert.ThrowsAsync<UnauthorizedAccessException>(() =>
            client.GetAsync<ApiResponse<SimpleData>>("/fake"));

        Assert.Equal(2, handler.CallCount);
    }
}




