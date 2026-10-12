using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingHeimdallAars;

/// <summary>
/// Exercises <see cref="HeimdallApiClient.GetLatestHeimdallAarAsync"/> end to end against a fake transport:
/// the query string for <c>include</c>, and deserialization of <c>at_span_id</c> and the per-span breakdown.
/// </summary>
[Trait("Category", "Unit")]
public class GetLatestHeimdallAar
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanA = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanB = Guid.Parse("22222222-2222-2222-2222-222222222222");

    private const string LineOnlyJson = """
        {
          "data": {
            "metric": "Heimdall AAR",
            "unit": "Ampere",
            "heimdall_aar": { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111" },
            "heimdall_span_aars": null
          }
        }
        """;

    private const string WithSpansJson = """
        {
          "data": {
            "metric": "Heimdall AAR",
            "unit": "Ampere",
            "heimdall_aar": { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111" },
            "heimdall_span_aars": [
              { "span_id": "11111111-1111-1111-1111-111111111111", "heimdall_aar": { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4 } },
              { "span_id": "22222222-2222-2222-2222-222222222222", "heimdall_aar": { "timestamp": "2026-01-01T12:00:00Z", "value": 412.8 } }
            ]
          }
        }
        """;

    [Fact]
    public async Task ShouldNotSendInclude_WhenNotSpecified()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallAarAsync(LineId);

        Assert.Null(QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task ShouldSendIncludeSpans_WhenSpecified()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallAarAsync(
            LineId, new() { Include = HeimdallAarInclude.Spans });

        Assert.Equal("spans", QueryString.Of(handler.LastRequest)["include"]);
    }

    [Fact]
    public async Task ShouldDeserializeAtSpanId()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallAarAsync(LineId);

        Assert.Equal(SpanA, result.HeimdallAar.AtSpanId);
    }

    [Fact]
    public async Task HeimdallSpanAarsShouldBeNull_WhenNotIncluded()
    {
        var handler = new RecordingHttpMessageHandler(LineOnlyJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallAarAsync(LineId);

        Assert.Equal(375.4, result.HeimdallAar.Value);
        Assert.Null(result.HeimdallSpanAars);
    }

    [Fact]
    public async Task ShouldDeserializeSpanBreakdown_WhenIncluded()
    {
        var handler = new RecordingHttpMessageHandler(WithSpansJson);

        var result = await HeimdallApiClientFactory.Create(handler).GetLatestHeimdallAarAsync(
            LineId, new() { Include = HeimdallAarInclude.Spans });

        Assert.Collection(result.HeimdallSpanAars!,
            first =>
            {
                Assert.Equal(SpanA, first.SpanId);
                Assert.Equal(new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero), first.HeimdallAar.Timestamp);
                Assert.Equal(375.4, first.HeimdallAar.Value);
            },
            second =>
            {
                Assert.Equal(SpanB, second.SpanId);
                Assert.Equal(412.8, second.HeimdallAar.Value);
            });
    }
}
