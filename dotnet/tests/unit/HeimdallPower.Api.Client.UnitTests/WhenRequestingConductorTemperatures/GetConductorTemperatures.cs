using HeimdallPower.Api.Client.GridInsights.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingConductorTemperatures;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetConductorTemperaturesAsync"/> end to end against a fake
/// transport: the query string sent for each option, and deserialization of the measurement point breakdown.
/// </summary>
[Trait("Category", "Unit")]
public class GetConductorTemperatures
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanId = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanPhaseId = Guid.Parse("33333333-3333-3333-3333-333333333333");
    private static readonly Guid MeasurementPointId = Guid.Parse("44444444-4444-4444-4444-444444444444");
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    private const string AggregateOnlyJson = """
        {
          "data": {
            "metric": "Conductor temperature",
            "unit": "C",
            "conductor_temperatures": [
              {
                "timestamp": "2026-01-01T12:00:00Z",
                "max": 68.7,
                "min": 55.2,
                "max_at_span_id": "11111111-1111-1111-1111-111111111111",
                "min_at_span_id": "22222222-2222-2222-2222-222222222222"
              }
            ],
            "measurement_point_temperatures": null
          }
        }
        """;

    private const string WithMeasurementPointsJson = """
        {
          "data": {
            "metric": "Conductor temperature",
            "unit": "C",
            "conductor_temperatures": [],
            "measurement_point_temperatures": [
              {
                "span_id": "11111111-1111-1111-1111-111111111111",
                "span_phases": [
                  {
                    "span_phase_id": "33333333-3333-3333-3333-333333333333",
                    "measurement_points": [
                      {
                        "measurement_point_id": "44444444-4444-4444-4444-444444444444",
                        "temperatures": [
                          { "timestamp": "2026-01-01T12:00:00Z", "value": 64.3 },
                          { "timestamp": "2026-01-01T12:05:00Z", "value": 65.1 }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldOmitInclude_WhenNotSpecified()
    {
        var handler = new RecordingHttpMessageHandler(AggregateOnlyJson);

        await HeimdallApiClientFactory.Create(handler).GetConductorTemperaturesAsync(LineId, From, To);

        var request = handler.LastRequest;
        Assert.Equal($"/grid_insights/v1/lines/{LineId}/conductor_temperatures", request.RequestUri!.AbsolutePath);
        var query = QueryString.Of(request);
        Assert.Equal("2026-01-01T00:00:00.0000000Z", query["from_timestamp"]);
        Assert.Equal("2026-01-02T00:00:00.0000000Z", query["to_timestamp"]);
        Assert.Equal("metric", query["unit_system"]);
        Assert.Null(query["include"]);
    }

    [Fact]
    public async Task ShouldSendInclude_WhenMeasurementPointsRequested()
    {
        var handler = new RecordingHttpMessageHandler(WithMeasurementPointsJson);

        await HeimdallApiClientFactory.Create(handler).GetConductorTemperaturesAsync(
            LineId, From, To, include: ConductorTemperatureInclude.MeasurementPoints);

        Assert.Equal("measurement_points", QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task ShouldDeserializeSpanIdsOfTheAggregate()
    {
        var handler = new RecordingHttpMessageHandler(AggregateOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetConductorTemperaturesAsync(LineId, From, To);

        var reading = Assert.Single(result.ConductorTemperatures);
        Assert.Equal(SpanId, reading.MaxAtSpanId);
        Assert.Equal(Guid.Parse("22222222-2222-2222-2222-222222222222"), reading.MinAtSpanId);
        Assert.Null(result.MeasurementPointTemperatures);
    }

    [Fact]
    public async Task ShouldDeserializeMeasurementPointTimeSeries_WhenIncluded()
    {
        var handler = new RecordingHttpMessageHandler(WithMeasurementPointsJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetConductorTemperaturesAsync(
            LineId, From, To, include: ConductorTemperatureInclude.MeasurementPoints);

        Assert.Empty(result.ConductorTemperatures);
        var span = Assert.Single(result.MeasurementPointTemperatures!);
        Assert.Equal(SpanId, span.SpanId);
        var spanPhase = Assert.Single(span.SpanPhases);
        Assert.Equal(SpanPhaseId, spanPhase.SpanPhaseId);
        var measurementPoint = Assert.Single(spanPhase.MeasurementPoints);
        Assert.Equal(MeasurementPointId, measurementPoint.MeasurementPointId);
        Assert.Collection(measurementPoint.Temperatures,
            first =>
            {
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero), first.Timestamp);
                Assert.Equal(64.3, first.Value);
            },
            second =>
            {
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 5, 0, TimeSpan.Zero), second.Timestamp);
                Assert.Equal(65.1, second.Value);
            });
    }
}
