using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingHeimdallDlrs;

/// <summary>
/// Verifies that the span at which the lowest ampacity was calculated deserializes on Heimdall DLR responses.
/// </summary>
[Trait("Category", "Unit")]
public class AtSpanId
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanA = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanB = Guid.Parse("22222222-2222-2222-2222-222222222222");

    [Fact]
    public async Task ShouldDeserializeAtSpanIdOnLatestHeimdallDlr()
    {
        const string json = """
            { "data": { "metric": "Heimdall DLR", "unit": "Ampere",
              "heimdall_dlr": { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111", "is_fallback": false } } }
            """;

        var result = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(json)).GetLatestHeimdallDlrAsync(LineId);

        Assert.Equal(SpanA, result.HeimdallDlr.AtSpanId);
    }

    [Fact]
    public async Task ShouldDeserializeAtSpanIdOnHistoricalHeimdallDlrs()
    {
        const string json = """
            { "data": { "metric": "Heimdall DLR", "unit": "Ampere", "heimdall_dlrs": [
              { "timestamp": "2026-01-01T12:00:00Z", "value": 375.4, "at_span_id": "11111111-1111-1111-1111-111111111111", "is_fallback": false },
              { "timestamp": "2026-01-01T12:05:00Z", "value": 380.0, "at_span_id": "22222222-2222-2222-2222-222222222222", "is_fallback": true } ] } }
            """;

        var result = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(json))
            .GetHeimdallDlrsAsync(LineId, DateTimeOffset.UnixEpoch, DateTimeOffset.UnixEpoch.AddDays(1));

        Assert.Equal([SpanA, SpanB], result.HeimdallDlrs.Select(dlr => dlr.AtSpanId));
    }
}
