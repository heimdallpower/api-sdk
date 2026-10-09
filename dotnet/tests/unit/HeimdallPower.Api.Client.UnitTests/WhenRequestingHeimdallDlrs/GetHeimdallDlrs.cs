using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingHeimdallDlrs;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetHeimdallDlrsAsync"/> end to end against a fake transport:
/// the query string for <c>include</c>, and deserialization of the per-span series.
/// </summary>
[Trait("Category", "Unit")]
public class GetHeimdallDlrs
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanA = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanB = Guid.Parse("22222222-2222-2222-2222-222222222222");
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    private const string LineOnlyJson = """
        {
          "data": {
            "metric": "Heimdall DLR",
            "unit": "Ampere",
            "heimdall_dlrs": [
              { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111", "is_fallback": false }
            ],
            "heimdall_span_dlrs": null
          }
        }
        """;

    private const string WithSpansJson = """
        {
          "data": {
            "metric": "Heimdall DLR",
            "unit": "Ampere",
            "heimdall_dlrs": [
              { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111", "is_fallback": false }
            ],
            "heimdall_span_dlrs": [
              {
                "span_id": "11111111-1111-1111-1111-111111111111",
                "heimdall_dlrs": [
                  { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "is_fallback": false },
                  { "timestamp": "2026-01-01T12:05:00Z", "value": 377.9, "is_fallback": false }
                ]
              },
              {
                "span_id": "22222222-2222-2222-2222-222222222222",
                "heimdall_dlrs": [
                  { "timestamp": "2026-01-01T12:00:00Z", "value": 412.8, "is_fallback": true }
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

        await HeimdallApiClientFactory.Create(handler).GetHeimdallDlrsAsync(LineId, From, To);

        Assert.Null(QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task ShouldSendIncludeSpans_WhenSpecified()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        await HeimdallApiClientFactory.Create(handler).GetHeimdallDlrsAsync(
            LineId, From, To, new() { Include = HeimdallDlrInclude.Spans });

        var query = QueryString.Of(handler.LastRequest);
        Assert.Equal("spans", query["include"]);
        Assert.Equal("current", query["quantity"]);
    }

    [Fact]
    public async Task HeimdallSpanDlrsShouldBeNull_WhenNotIncluded()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetHeimdallDlrsAsync(LineId, From, To);

        Assert.Single(result.HeimdallDlrs);
        Assert.Null(result.HeimdallSpanDlrs);
    }

    [Fact]
    public async Task ShouldDeserializeSpanSeries_WhenIncluded()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetHeimdallDlrsAsync(
            LineId, From, To, new() { Include = HeimdallDlrInclude.Spans });

        Assert.Collection(result.HeimdallSpanDlrs!,
            first =>
            {
                Assert.Equal(SpanA, first.SpanId);
                Assert.Equal([375.4, 377.9], first.HeimdallDlrs.Select(dlr => dlr.Value));
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 5, 0, TimeSpan.Zero), first.HeimdallDlrs[1].Timestamp);
            },
            second =>
            {
                Assert.Equal(SpanB, second.SpanId);
                var dlr = Assert.Single(second.HeimdallDlrs);
                Assert.True(dlr.IsFallback);
            });
    }
}
