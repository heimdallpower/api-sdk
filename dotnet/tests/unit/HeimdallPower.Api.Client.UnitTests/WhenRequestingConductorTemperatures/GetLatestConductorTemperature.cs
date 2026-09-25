using HeimdallPower.Api.Client.GridInsights.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingConductorTemperatures;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetLatestConductorTemperatureAsync"/> end to end against a fake
/// transport: the query string sent for each option, and deserialization of the measurement point breakdown.
/// </summary>
[Trait("Category", "Unit")]
public class GetLatestConductorTemperature
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid MaxSpanId = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid MinSpanId = Guid.Parse("22222222-2222-2222-2222-222222222222");
    private static readonly Guid SpanPhaseId = Guid.Parse("33333333-3333-3333-3333-333333333333");
    private static readonly Guid MeasurementPointA = Guid.Parse("44444444-4444-4444-4444-444444444444");
    private static readonly Guid MeasurementPointB = Guid.Parse("55555555-5555-5555-5555-555555555555");

    private const string AggregateOnlyJson = """
        {
          "data": {
            "metric": "Conductor temperature",
            "unit": "C",
            "conductor_temperature": {
              "timestamp": "2026-01-01T12:00:00Z",
              "max": 68.7,
              "min": 55.2,
              "max_at_span_id": "11111111-1111-1111-1111-111111111111",
              "min_at_span_id": "22222222-2222-2222-2222-222222222222"
            },
            "measurement_point_temperatures": null
          }
        }
        """;

    private const string WithMeasurementPointsJson = """
        {
          "data": {
            "metric": "Conductor temperature",
            "unit": "C",
            "conductor_temperature": {
              "timestamp": "2026-01-01T12:00:00Z",
              "max": 68.7,
              "min": null,
              "max_at_span_id": "11111111-1111-1111-1111-111111111111",
              "min_at_span_id": null
            },
            "measurement_point_temperatures": [
              {
                "span_id": "11111111-1111-1111-1111-111111111111",
                "span_phases": [
                  {
                    "span_phase_id": "33333333-3333-3333-3333-333333333333",
                    "measurement_points": [
                      { "measurement_point_id": "44444444-4444-4444-4444-444444444444", "timestamp": "2026-01-01T11:58:00Z", "value": 64.3 },
                      { "measurement_point_id": "55555555-5555-5555-5555-555555555555", "timestamp": "2026-01-01T11:59:00Z", "value": 68.7 }
                    ]
                  }
                ]
              }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldOmitSinceAndInclude_WhenNotSpecified()
    {
        var handler = new RecordingHttpMessageHandler(AggregateOnlyJson);

        await HeimdallApiClientFactory.Create(handler).GetLatestConductorTemperatureAsync(LineId);

        var request = handler.LastRequest;
        Assert.Equal($"/grid_insights/v1/lines/{LineId}/conductor_temperatures/latest", request.RequestUri!.AbsolutePath);
        var query = QueryString.Of(request);
        Assert.Equal("metric", query["unit_system"]);
        Assert.Null(query["since"]);
        Assert.Null(query["include"]);
    }

    [Fact]
    public async Task ShouldSendSinceAndInclude_WhenSpecified()
    {
        var handler = new RecordingHttpMessageHandler(WithMeasurementPointsJson);
        var since = new DateTimeOffset(2026, 1, 1, 13, 30, 0, TimeSpan.FromHours(1));

        await HeimdallApiClientFactory.Create(handler).GetLatestConductorTemperatureAsync(
            LineId, unitSystem: "imperial", since: since, include: ConductorTemperatureInclude.MeasurementPoints);

        var query = QueryString.Of(handler.LastRequest);
        Assert.Equal("imperial", query["unit_system"]);
        Assert.Equal("2026-01-01T12:30:00.0000000Z", query["since"]);
        Assert.Equal("measurement_points", query["include"]);
    }

    [Fact]
    public async Task ShouldDeserializeSpanIdsOfTheAggregate()
    {
        var handler = new RecordingHttpMessageHandler(AggregateOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestConductorTemperatureAsync(LineId);

        Assert.Equal(MaxSpanId, result.ConductorTemperature.MaxAtSpanId);
        Assert.Equal(MinSpanId, result.ConductorTemperature.MinAtSpanId);
    }

    [Fact]
    public async Task MeasurementPointTemperaturesShouldBeNull_WhenNotIncluded()
    {
        var handler = new RecordingHttpMessageHandler(AggregateOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestConductorTemperatureAsync(LineId);

        Assert.Null(result.MeasurementPointTemperatures);
    }

    [Fact]
    public async Task ShouldDeserializeMeasurementPointBreakdown_WhenIncluded()
    {
        var handler = new RecordingHttpMessageHandler(WithMeasurementPointsJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestConductorTemperatureAsync(
            LineId, include: ConductorTemperatureInclude.MeasurementPoints);

        Assert.Null(result.ConductorTemperature.Min);
        Assert.Null(result.ConductorTemperature.MinAtSpanId);

        var span = Assert.Single(result.MeasurementPointTemperatures!);
        Assert.Equal(MaxSpanId, span.SpanId);
        var spanPhase = Assert.Single(span.SpanPhases);
        Assert.Equal(SpanPhaseId, spanPhase.SpanPhaseId);
        Assert.Collection(spanPhase.MeasurementPoints,
            first =>
            {
                Assert.Equal(MeasurementPointA, first.MeasurementPointId);
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 11, 58, 0, TimeSpan.Zero), first.Timestamp);
                Assert.Equal(64.3, first.Value);
            },
            second =>
            {
                Assert.Equal(MeasurementPointB, second.MeasurementPointId);
                Assert.Equal(68.7, second.Value);
            });
    }
}
