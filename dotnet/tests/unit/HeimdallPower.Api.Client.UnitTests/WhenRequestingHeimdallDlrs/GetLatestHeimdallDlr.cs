using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingHeimdallDlrs;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetLatestHeimdallDlrAsync"/> end to end against a fake transport:
/// the query string for <c>include</c>, and deserialization of the per-span breakdown.
/// </summary>
[Trait("Category", "Unit")]
public class GetLatestHeimdallDlr
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanA = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanB = Guid.Parse("22222222-2222-2222-2222-222222222222");

    private const string LineOnlyJson = """
        {
          "data": {
            "metric": "Heimdall DLR",
            "unit": "Ampere",
            "heimdall_dlr": { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111", "is_fallback": false },
            "heimdall_span_dlrs": null
          }
        }
        """;

    private const string WithSpansJson = """
        {
          "data": {
            "metric": "Heimdall DLR",
            "unit": "Ampere",
            "heimdall_dlr": { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111", "is_fallback": false },
            "heimdall_span_dlrs": [
              { "span_id": "11111111-1111-1111-1111-111111111111", "heimdall_dlr": { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "is_fallback": false } },
              { "span_id": "22222222-2222-2222-2222-222222222222", "heimdall_dlr": { "timestamp": "2026-01-01T12:00:00Z", "value": 412.8, "is_fallback": true } }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldNotSendInclude_WhenNotSpecified()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallDlrAsync(LineId);

        Assert.Null(QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task ShouldSendIncludeSpans_WhenSpecified()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallDlrAsync(
            LineId, new() { Include = HeimdallDlrInclude.Spans });

        Assert.Equal("spans", QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task HeimdallSpanDlrsShouldBeNull_WhenNotIncluded()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallDlrAsync(LineId);

        Assert.Equal(375.4, result.HeimdallDlr.Value);
        Assert.Null(result.HeimdallSpanDlrs);
    }

    [Fact]
    public async Task ShouldDeserializeSpanBreakdown_WhenIncluded()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallDlrAsync(
            LineId, new() { Include = HeimdallDlrInclude.Spans });

        Assert.Collection(result.HeimdallSpanDlrs!,
            first =>
            {
                Assert.Equal(SpanA, first.SpanId);
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero), first.HeimdallDlr.Timestamp);
                Assert.Equal(375.4, first.HeimdallDlr.Value);
                Assert.False(first.HeimdallDlr.IsFallback);
            },
            second =>
            {
                Assert.Equal(SpanB, second.SpanId);
                Assert.Equal(412.8, second.HeimdallDlr.Value);
                Assert.True(second.HeimdallDlr.IsFallback);
            });
    }
}
