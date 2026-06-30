using System.Net;
using HeimdallPower.Api.Client.GridInsights.Lines;
using HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses;

/// <summary>
/// Verifies that HeimdallApiHttpClient handles HTTP 404 Not Found correctly.
///
/// Latest endpoints (e.g. /currents/latest, /heimdall_dlrs/latest) return 404
/// when no recent data is available for a line — this is a non-transient,
/// non-retryable condition and must surface as HeimdallApiException(NotFound).
/// </summary>
[Trait("Category", "Unit")]
public class WhenApiReturnsNotFound
{
    private const string Url = "https://fake-api.example.com/v1/test";

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns404WithJsonBody()
    {
        const string problemJson =
            """{"title":"Not Found","detail":"No data available for this line","status":404}""";

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.NotFound, problemJson));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.NotFound, ex.StatusCode);
        Assert.Contains("No data available for this line", ex.Message);
    }

    [Fact]
    public async Task ShouldThrowHeimdallApiException_WhenServerReturns404WithEmptyBody()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsEmpty(HttpStatusCode.NotFound));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.NotFound, ex.StatusCode);
    }

    [Fact]
    public async Task StatusCodeShouldBeNotFound_WhenServerReturns404()
    {
        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.NotFound,
                """{"title":"Not Found","status":404}"""));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() =>
            client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.NotFound, ex.StatusCode);
    }
}

