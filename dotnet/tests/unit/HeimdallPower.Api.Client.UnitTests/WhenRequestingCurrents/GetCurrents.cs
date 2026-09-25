using HeimdallPower.Api.Client.GridInsights.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingCurrents;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetCurrentsAsync"/> end to end against a fake transport:
/// the <c>include</c> query parameter and deserialization of the per-measurement-point time series.
/// </summary>
[Trait("Category", "Unit")]
public class GetCurrents
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid MeasurementPointId = Guid.Parse("44444444-4444-4444-4444-444444444444");
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    private const string Json = """
        {
          "data": {
            "metric": "Current",
            "unit": "Ampere",
            "currents": [ { "timestamp": "2026-01-01T12:00:00Z", "value": 452.3 } ],
            "measurement_point_currents": [
              {
                "span_id": "11111111-1111-1111-1111-111111111111",
                "span_phases": [
                  {
                    "span_phase_id": "33333333-3333-3333-3333-333333333333",
                    "measurement_points": [
                      {
                        "measurement_point_id": "44444444-4444-4444-4444-444444444444",
                        "currents": [
                          { "timestamp": "2026-01-01T12:00:00Z", "value": 450.1 },
                          { "timestamp": "2026-01-01T12:05:00Z", "value": 452.3 }
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
        var handler = new RecordingHttpMessageHandler(Json);

        await HeimdallApiClientFactory.Create(handler).GetCurrentsAsync(LineId, From, To);

        var query = QueryString.Of(handler.LastRequest);
        Assert.Equal("2026-01-01T00:00:00.0000000Z", query["from_timestamp"]);
        Assert.Equal("2026-01-02T00:00:00.0000000Z", query["to_timestamp"]);
        Assert.Null(query["include"]);
    }

    [Fact]
    public async Task ShouldSendInclude_WhenMeasurementPointsRequested()
    {
        var handler = new RecordingHttpMessageHandler(Json);

        await HeimdallApiClientFactory.Create(handler).GetCurrentsAsync(LineId, From, To, include: CurrentInclude.MeasurementPoints);

        Assert.Equal("measurement_points", QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task ShouldDeserializeMeasurementPointTimeSeries()
    {
        var handler = new RecordingHttpMessageHandler(Json);

        var result = await HeimdallApiClientFactory.Create(handler).GetCurrentsAsync(LineId, From, To, include: CurrentInclude.MeasurementPoints);

        var measurementPoint = Assert.Single(Assert.Single(Assert.Single(result.MeasurementPointCurrents!).SpanPhases).MeasurementPoints);
        Assert.Equal(MeasurementPointId, measurementPoint.MeasurementPointId);
        Assert.Collection(measurementPoint.Currents,
            first =>
            {
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero), first.Timestamp);
                Assert.Equal(450.1, first.Value);
            },
            second =>
            {
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 5, 0, TimeSpan.Zero), second.Timestamp);
                Assert.Equal(452.3, second.Value);
            });
    }
}
