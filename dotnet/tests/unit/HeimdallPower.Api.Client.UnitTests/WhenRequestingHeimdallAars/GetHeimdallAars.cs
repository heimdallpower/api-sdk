using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingHeimdallAars;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetHeimdallAarsAsync"/> end to end against a fake transport:
/// the query string for <c>include</c>, and deserialization of <c>at_span_id</c> and the per-span series.
/// </summary>
[Trait("Category", "Unit")]
public class GetHeimdallAars
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanA = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanB = Guid.Parse("22222222-2222-2222-2222-222222222222");
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    private const string LineOnlyJson = """
        {
          "data": {
            "metric": "Heimdall AAR",
            "unit": "Ampere",
            "heimdall_aars": [
              { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111" },
              { "timestamp": "2026-01-01T12:05:00Z", "value": 380.0, "at_span_id": "22222222-2222-2222-2222-222222222222" }
            ],
            "heimdall_span_aars": null
          }
        }
        """;

    private const string WithSpansJson = """
        {
          "data": {
            "metric": "Heimdall AAR",
            "unit": "Ampere",
            "heimdall_aars": [
              { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111" }
            ],
            "heimdall_span_aars": [
              {
                "span_id": "11111111-1111-1111-1111-111111111111",
                "heimdall_aars": [
                  { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4 },
                  { "timestamp": "2026-01-01T12:05:00Z", "value": 377.9 }
                ]
              },
              {
                "span_id": "22222222-2222-2222-2222-222222222222",
                "heimdall_aars": [
                  { "timestamp": "2026-01-01T12:00:00Z", "value": 412.8 }
                ]
              }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldNotSendInclude_WhenNotSpecified()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        await HeimdallApiClientFactory.Create(handler).GetHeimdallAarsAsync(LineId, From, To);

        Assert.Null(QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task ShouldSendIncludeSpans_WhenSpecified()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        await HeimdallApiClientFactory.Create(handler).GetHeimdallAarsAsync(
            LineId, From, To, new() { Include = HeimdallAarInclude.Spans });

        var query = QueryString.Of(handler.LastRequest);
        Assert.Equal("spans", query["include"]);
        Assert.Equal("current", query["quantity"]);
    }

    [Fact]
    public async Task ShouldDeserializeAtSpanId()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetHeimdallAarsAsync(LineId, From, To);

        Assert.Equal([SpanA, SpanB], result.HeimdallAars.Select(aar => aar.AtSpanId));
    }

    [Fact]
    public async Task HeimdallSpanAarsShouldBeNull_WhenNotIncluded()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetHeimdallAarsAsync(LineId, From, To);

        Assert.Equal(2, result.HeimdallAars.Count);
        Assert.Null(result.HeimdallSpanAars);
    }

    [Fact]
    public async Task ShouldDeserializeSpanSeries_WhenIncluded()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetHeimdallAarsAsync(
            LineId, From, To, new() { Include = HeimdallAarInclude.Spans });

        Assert.Collection(result.HeimdallSpanAars!,
            first =>
            {
                Assert.Equal(SpanA, first.SpanId);
                Assert.Equal([375.4, 377.9], first.HeimdallAars.Select(aar => aar.Value));
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 5, 0, TimeSpan.Zero), first.HeimdallAars[1].Timestamp);
            },
            second =>
            {
                Assert.Equal(SpanB, second.SpanId);
                var aar = Assert.Single(second.HeimdallAars);
                Assert.Equal(412.8, aar.Value);
            });
    }
}
