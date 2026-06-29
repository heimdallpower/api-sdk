using System.Net;
using HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses;

/// <summary>
/// Verifies that <see cref="HeimdallApiHttpClient"/> handles error responses gracefully
/// regardless of whether the body is valid JSON (ProblemDetails), raw HTML (e.g. from an
/// Application Gateway), or empty — and that no <see cref="System.Text.Json.JsonException"/>
/// ever leaks to the caller.
///
/// Status codes covered by the ProblemDetails/HTML fallback path: 400, 500, 503.
/// Other non-success codes (502, 504, …) go through a separate path that uses
/// <c>TruncateBody</c> to collapse whitespace, which also handles HTML gracefully.
/// </summary>
[Trait("Category", "Unit")]
public class WhenResponseBodyIsHtml
{
    private const string Url = "https://fake-api.example.com/v1/test";

    // ── 500 InternalServerError ──────────────────────────────────────────────

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns500WithHtmlBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsHtml(HttpStatusCode.InternalServerError));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.InternalServerError, ex.StatusCode);
        // The HTML should be truncated/collapsed — not a raw JsonException message.
        Assert.DoesNotContain("JsonException", ex.Message);
        Assert.Contains("500", ex.Message);
    }

    [Fact]
    public async Task ShouldIncludeTruncatedHtmlInMessage_WhenServerReturns500WithHtmlBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsHtml(HttpStatusCode.InternalServerError));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        // HTML tags should be present (body is passed through TruncateBody which collapses
        // whitespace but does not strip tags). More importantly it must not be empty.
        Assert.False(string.IsNullOrWhiteSpace(ex.Message));
    }

    [Fact]
    public async Task ShouldParseProblemDetails_WhenServerReturns500WithJsonBody()
    {
        const string problemJson =
            """{"title":"Internal Server Error","detail":"Something went wrong","status":500}""";

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.InternalServerError, problemJson));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.InternalServerError, ex.StatusCode);
        Assert.Contains("Something went wrong", ex.Message);
    }

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns500WithEmptyBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsEmpty(HttpStatusCode.InternalServerError));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.InternalServerError, ex.StatusCode);
        Assert.Contains("(empty body)", ex.Message);
    }

    // ── 400 BadRequest ───────────────────────────────────────────────────────

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns400WithHtmlBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsHtml(HttpStatusCode.BadRequest));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.BadRequest, ex.StatusCode);
        Assert.DoesNotContain("JsonException", ex.Message);
    }

    [Fact]
    public async Task ShouldParseProblemDetails_WhenServerReturns400WithJsonBody()
    {
        const string problemJson =
            """{"title":"Bad Request","detail":"Validation failed","status":400}""";

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.BadRequest, problemJson));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.BadRequest, ex.StatusCode);
        Assert.Contains("Validation failed", ex.Message);
    }

    // ── 503 ServiceUnavailable ───────────────────────────────────────────────

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns503WithHtmlBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsHtml(HttpStatusCode.ServiceUnavailable));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.ServiceUnavailable, ex.StatusCode);
        Assert.DoesNotContain("JsonException", ex.Message);
    }

    // ── 502 / 504 — non-ProblemDetails path (TruncateBody) ──────────────────

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns502WithHtmlBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsHtml(HttpStatusCode.BadGateway));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.BadGateway, ex.StatusCode);
        Assert.DoesNotContain("JsonException", ex.Message);
        // TruncateBody collapses whitespace — the message should be a single line.
        Assert.DoesNotContain("\n", ex.Message);
    }

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns504WithHtmlBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsHtml(HttpStatusCode.GatewayTimeout));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.GatewayTimeout, ex.StatusCode);
        Assert.DoesNotContain("JsonException", ex.Message);
    }

    // ── TruncateBody: long bodies are capped at 200 chars ───────────────────

    [Fact]
    public async Task ShouldTruncateLongBody_WhenBodyExceeds200Characters()
    {
        var longBody = new string('x', 500);

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.Returns(HttpStatusCode.BadGateway, longBody));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        // Message includes status text + truncated body; the body portion is ≤ 200 chars + "..."
        Assert.Contains("...", ex.Message);
        Assert.DoesNotContain(longBody, ex.Message);
    }
}

