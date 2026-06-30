using System.Net;
using HeimdallPower.Api.Client.GridInsights.Lines;
using HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses;

/// <summary>
/// Verifies that HeimdallApiHttpClient deserializes a successful (200 OK) response
/// into the expected strongly-typed model — no network calls, no auth.
///
/// Uses snake_case JSON that mirrors the real API contract so the tests also
/// act as a guard against accidental serialisation regressions.
/// </summary>
[Trait("Category", "Unit")]
public class WhenApiReturnsSuccess
{
    private const string Url = "https://fake-api.example.com/v1/test";

    [Fact]
    public async Task ShouldDeserializeLatestCurrentResponse()
    {
        const string json = """
            {
              "data": {
                "metric": "Current",
                "unit": "Ampere",
                "current": {
                  "timestamp": "2026-01-01T12:00:00Z",
                  "value": 500.5
                }
              }
            }
            """;

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.OK, json));

        var result = await client.GetAsync<ApiResponse<LatestCurrentResponse>>(Url);

        Assert.NotNull(result);
        Assert.Equal("Current", result.Data.Metric);
        Assert.Equal("Ampere", result.Data.Unit);
        Assert.Equal(500.5, result.Data.Current.Value);
        Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero), result.Data.Current.Timestamp);
    }

    [Fact]
    public async Task ShouldDeserializeLatestConductorTemperatureResponse()
    {
        const string json = """
            {
              "data": {
                "metric": "Conductor temperature",
                "unit": "C",
                "conductor_temperature": {
                  "timestamp": "2026-01-01T12:00:00Z",
                  "max": 68.7,
                  "min": 55.2
                }
              }
            }
            """;

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.OK, json));

        var result = await client.GetAsync<ApiResponse<LatestConductorTemperatureResponse>>(Url);

        Assert.NotNull(result);
        Assert.Equal("Conductor temperature", result.Data.Metric);
        Assert.Equal("C", result.Data.Unit);
        Assert.Equal(68.7, result.Data.ConductorTemperature.Max);
        Assert.Equal(55.2, result.Data.ConductorTemperature.Min);
    }
}

