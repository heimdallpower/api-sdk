using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingCurrents;

/// <summary>
/// Verifies that the span where the line current was measured deserializes on the current and apparent power responses.
/// </summary>
[Trait("Category", "Unit")]
public class AtSpanId
{
    private static readonly Guid LineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly Guid SpanA = Guid.Parse("11111111-1111-1111-1111-111111111111");
    private static readonly Guid SpanB = Guid.Parse("22222222-2222-2222-2222-222222222222");

    [Fact]
    public async Task ShouldDeserializeAtSpanIdOnLatestCurrent()
    {
        const string json = """
            { "data": { "metric": "Current", "unit": "Ampere",
              "current": { "timestamp": "2026-01-01T12:00:00Z", "value": 452.3, "at_span_id": "11111111-1111-1111-1111-111111111111" } } }
            """;

        var result = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(json)).GetLatestCurrentAsync(LineId);

        Assert.Equal(SpanA, result.Current.AtSpanId);
    }

    [Fact]
    public async Task ShouldDeserializeAtSpanIdOnHistoricalCurrents()
    {
        const string json = """
            { "data": { "metric": "Current", "unit": "Ampere", "currents": [
              { "timestamp": "2026-01-01T12:00:00Z", "value": 452.3, "at_span_id": "11111111-1111-1111-1111-111111111111" },
              { "timestamp": "2026-01-01T12:05:00Z", "value": 460.0, "at_span_id": "22222222-2222-2222-2222-222222222222" } ] } }
            """;

        var result = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(json))
            .GetCurrentsAsync(LineId, DateTimeOffset.UnixEpoch, DateTimeOffset.UnixEpoch.AddDays(1));

        Assert.Equal([SpanA, SpanB], result.Currents.Select(current => current.AtSpanId));
    }

    [Fact]
    public async Task ShouldDeserializeAtSpanIdOnLatestApparentPower()
    {
        const string json = """
            { "data": { "metric": "Apparent power", "unit": "MVA",
              "apparent_power": { "timestamp": "2026-01-01T12:00:00Z", "value": 156.7, "at_span_id": "22222222-2222-2222-2222-222222222222" } } }
            """;

        var result = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(json)).GetLatestApparentPowerAsync(LineId);

        Assert.Equal(SpanB, result.ApparentPower.AtSpanId);
    }

    [Fact]
    public async Task ShouldDeserializeAtSpanIdOnHistoricalApparentPowers()
    {
        const string json = """
            { "data": { "metric": "Apparent power", "unit": "MVA", "apparent_powers": [
              { "timestamp": "2026-01-01T12:00:00Z", "value": 156.7, "at_span_id": "11111111-1111-1111-1111-111111111111" },
              { "timestamp": "2026-01-01T12:05:00Z", "value": 159.4, "at_span_id": "22222222-2222-2222-2222-222222222222" } ] } }
            """;

        var result = await HeimdallApiClientFactory.Create(new RecordingHttpMessageHandler(json))
            .GetApparentPowersAsync(LineId, DateTimeOffset.UnixEpoch, DateTimeOffset.UnixEpoch.AddDays(1));

        Assert.Equal([SpanA, SpanB], result.ApparentPowers.Select(apparentPower => apparentPower.AtSpanId));
    }
}
