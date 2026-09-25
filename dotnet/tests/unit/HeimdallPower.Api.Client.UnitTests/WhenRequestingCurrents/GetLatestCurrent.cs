using HeimdallPower.Api.Client.GridInsights.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingCurrents;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetLatestCurrentAsync"/> end to end against a fake transport:
/// the query string for <c>since</c> and <c>include</c>, and deserialization of the measurement point breakdown.
/// </summary>
[Trait("Category", "Unit")]
public class GetLatestCurrent
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanId = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanPhaseId = Guid.Parse("33333333-3333-3333-3333-333333333333");
    private static readonly Guid MeasurementPointA = Guid.Parse("44444444-4444-4444-4444-444444444444");
    private static readonly Guid MeasurementPointB = Guid.Parse("55555555-5555-5555-5555-555555555555");

    private const string AggregateOnlyJson = """
        {
          "data": {
            "metric": "Current",
            "unit": "Ampere",
            "current": { "timestamp": "2026-01-01T12:00:00Z", "value": 452.3 },
            "measurement_point_currents": null
          }
        }
        """;

    private const string WithMeasurementPointsJson = """
        {
          "data": {
            "metric": "Current",
            "unit": "Ampere",
            "current": { "timestamp": "2026-01-01T12:00:00Z", "value": 452.3 },
            "measurement_point_currents": [
              {
                "span_id": "11111111-1111-1111-1111-111111111111",
                "span_phases": [
                  {
                    "span_phase_id": "33333333-3333-3333-3333-333333333333",
                    "measurement_points": [
                      { "measurement_point_id": "44444444-4444-4444-4444-444444444444", "timestamp": "2026-01-01T11:58:00Z", "value": 450.1 },
                      { "measurement_point_id": "55555555-5555-5555-5555-555555555555", "timestamp": "2026-01-01T11:59:00Z", "value": 452.3 }
                    ]
                  }
                ]
              }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldSendNoQueryString_WhenNoOptionsSpecified()
    {
        var handler = new RecordingHttpMessageHandler(AggregateOnlyJson);

        await HeimdallApiClientFactory.Create(handler).GetLatestCurrentAsync(LineId);

        var uri = handler.LastRequest.RequestUri!;
        Assert.Equal($"/grid_insights/v1/lines/{LineId}/currents/latest", uri.AbsolutePath);
        Assert.Equal(string.Empty, uri.Query);
    }

    [Fact]
    public async Task ShouldSendSinceAndInclude_WhenSpecified()
    {
        var handler = new RecordingHttpMessageHandler(WithMeasurementPointsJson);
        var since = new DateTimeOffset(2026, 1, 1, 13, 30, 0, TimeSpan.FromHours(1));

        await HeimdallApiClientFactory.Create(handler).GetLatestCurrentAsync(
            LineId, since: since, include: CurrentInclude.MeasurementPoints);

        var query = QueryString.Of(handler.LastRequest);
        Assert.Equal("2026-01-01T12:30:00.0000000Z", query["since"]);
        Assert.Equal("measurement_points", query["include"]);
    }

    [Fact]
    public async Task MeasurementPointCurrentsShouldBeNull_WhenNotIncluded()
    {
        var handler = new RecordingHttpMessageHandler(AggregateOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestCurrentAsync(LineId);

        Assert.Equal(452.3, result.Current.Value);
        Assert.Null(result.MeasurementPointCurrents);
    }

    [Fact]
    public async Task ShouldDeserializeMeasurementPointBreakdown_WhenIncluded()
    {
        var handler = new RecordingHttpMessageHandler(WithMeasurementPointsJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestCurrentAsync(
            LineId, include: CurrentInclude.MeasurementPoints);

        var span = Assert.Single(result.MeasurementPointCurrents!);
        Assert.Equal(SpanId, span.SpanId);
        var spanPhase = Assert.Single(span.SpanPhases);
        Assert.Equal(SpanPhaseId, spanPhase.SpanPhaseId);
        Assert.Collection(spanPhase.MeasurementPoints,
            first =>
            {
                Assert.Equal(MeasurementPointA, first.MeasurementPointId);
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 11, 58, 0, TimeSpan.Zero), first.Timestamp);
                Assert.Equal(450.1, first.Value);
            },
            second =>
            {
                Assert.Equal(MeasurementPointB, second.MeasurementPointId);
                Assert.Equal(452.3, second.Value);
            });
    }
}
