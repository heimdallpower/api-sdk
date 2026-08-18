using System.Net;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
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

    [Fact]
    public async Task ShouldDeserializeLatestLineTransientRatingResponse()
    {
        const string json = """
            {
              "data": {
                "metric": "Line transient rating",
                "unit": "Ampere",
                "line_transient_rating": {
                  "timestamp": "2026-01-01T12:00:00Z",
                  "ratings": [
                    { "duration_minutes": 5, "value": 700.1 },
                    { "duration_minutes": 15, "value": 620.5 }
                  ]
                }
              }
            }
            """;

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.OK, json));

        var result = await client.GetAsync<ApiResponse<LatestLineTransientRatingResponse>>(Url);

        Assert.NotNull(result);
        Assert.Equal("Line transient rating", result.Data.Metric);
        Assert.Equal("Ampere", result.Data.Unit);
        Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero), result.Data.LineTransientRating.Timestamp);
        Assert.Equal(2, result.Data.LineTransientRating.Ratings.Count);
        Assert.Equal(5, result.Data.LineTransientRating.Ratings[0].DurationMinutes);
        Assert.Equal(700.1, result.Data.LineTransientRating.Ratings[0].Value);
        Assert.Equal(15, result.Data.LineTransientRating.Ratings[1].DurationMinutes);
        Assert.Equal(620.5, result.Data.LineTransientRating.Ratings[1].Value);
    }

    [Fact]
    public async Task ShouldDeserializeLatestCircuitTransientRatingResponse()
    {
        const string json = """
            {
              "data": {
                "metric": "Circuit transient rating",
                "unit": "Ampere",
                "circuit_transient_rating": {
                  "timestamp": "2026-01-01T12:00:00Z",
                  "ratings": [
                    { "duration_minutes": 5, "value": 650.0, "limiting_component_id": "1e0a4b0d-9b6c-4b8e-9f6a-2c3d4e5f6a7b" },
                    { "duration_minutes": 15, "value": 590.2, "limiting_component_id": null }
                  ]
                }
              }
            }
            """;

        var client = HeimdallApiHttpClientFactory.Create(
            FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.OK, json));

        var result = await client.GetAsync<ApiResponse<LatestCircuitTransientRatingResponse>>(Url);

        Assert.NotNull(result);
        Assert.Equal("Circuit transient rating", result.Data.Metric);
        Assert.Equal("Ampere", result.Data.Unit);
        Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero), result.Data.CircuitTransientRating.Timestamp);
        Assert.Equal(2, result.Data.CircuitTransientRating.Ratings.Count);
        Assert.Equal(5, result.Data.CircuitTransientRating.Ratings[0].DurationMinutes);
        Assert.Equal(650.0, result.Data.CircuitTransientRating.Ratings[0].Value);
        Assert.Equal(Guid.Parse("1e0a4b0d-9b6c-4b8e-9f6a-2c3d4e5f6a7b"), result.Data.CircuitTransientRating.Ratings[0].LimitingComponentId);
        // A null limiting component id means the line transient rating is the binding constraint.
        Assert.Null(result.Data.CircuitTransientRating.Ratings[1].LimitingComponentId);
    }
}

