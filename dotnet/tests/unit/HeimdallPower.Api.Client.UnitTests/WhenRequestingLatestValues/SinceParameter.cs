using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingLatestValues;

/// <summary>
/// Every "Get latest" endpoint accepts an optional <c>since</c> cut-off. These tests call each client
/// method through a fake transport and assert that <c>since</c> is sent as an ISO 8601 UTC timestamp
/// when given and omitted otherwise.
/// </summary>
[Trait("Category", "Unit")]
public class SinceParameter
{
    private static readonly Guid Id = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly DateTimeOffset Since = new(2026, 1, 1, 13, 30, 0, TimeSpan.FromHours(1));
    private const string ExpectedSince = "2026-01-01T12:30:00.0000000Z";

    private const string ValueJson = """{ "timestamp": "2026-01-01T12:00:00Z", "value": 1.0 }""";

    public static TheoryData<string, string, Func<HeimdallApiClient, DateTimeOffset?, Task>> Endpoints => new()
    {
        {
            "current", $$"""{ "data": { "metric": "Current", "unit": "Ampere", "current": {{ValueJson}} } }""",
            (client, since) => client.GetLatestCurrentAsync(Id, since: since)
        },
        {
            "apparent power", $$"""{ "data": { "metric": "Apparent power", "unit": "MVA", "apparent_power": {{ValueJson}} } }""",
            (client, since) => client.GetLatestApparentPowerAsync(Id, since: since)
        },
        {
            "Heimdall DLR", """{ "data": { "metric": "Heimdall DLR", "unit": "Ampere", "heimdall_dlr": { "timestamp": "2026-01-01T12:00:00Z", "value": 1.0, "at_span_id": "11111111-1111-1111-1111-111111111111", "is_fallback": false } } }""",
            (client, since) => client.GetLatestHeimdallDlrAsync(Id, since: since)
        },
        {
            "Heimdall AAR", $$"""{ "data": { "metric": "Heimdall AAR", "unit": "Ampere", "heimdall_aar": {{ValueJson}} } }""",
            (client, since) => client.GetLatestHeimdallAarAsync(Id, since: since)
        },
        {
            "circuit rating", """{ "data": { "metric": "Circuit rating", "unit": "Ampere", "circuit_rating": { "timestamp": "2026-01-01T12:00:00Z", "value": 1.0, "is_fallback": false } } }""",
            (client, since) => client.GetLatestCircuitRatingAsync(Id, Quantity.ApparentPower, since)
        },
        {
            "sag and clearance", """{ "data": { "metric": "SagAndClearance", "unit": "Multiple", "sag_and_clearance": { "max_sag": { "timestamp": "2026-01-01T12:00:00Z", "span_phase_id": "33333333-3333-3333-3333-333333333333", "value": 8.1, "unit": "m" }, "min_clearance": null, "spans": [] } } }""",
            (client, since) => client.GetLatestSagAndClearanceAsync(Id, since: since)
        },
    };

    [Theory]
    [MemberData(nameof(Endpoints))]
    public async Task ShouldSendSinceAsIsoUtcTimestamp_WhenSpecified(string endpoint, string json, Func<HeimdallApiClient, DateTimeOffset?, Task> call)
    {
        var handler = new RecordingHttpMessageHandler(json);

        await call(HeimdallApiClientFactory.Create(handler), Since);

        Assert.True(ExpectedSince == QueryString.Of(handler.LastRequest)["since"], $"{endpoint}: unexpected since in {handler.LastRequest.RequestUri}");
    }

    [Theory]
    [MemberData(nameof(Endpoints))]
    public async Task ShouldOmitSince_WhenNotSpecified(string endpoint, string json, Func<HeimdallApiClient, DateTimeOffset?, Task> call)
    {
        var handler = new RecordingHttpMessageHandler(json);

        await call(HeimdallApiClientFactory.Create(handler), null);

        Assert.True(QueryString.Of(handler.LastRequest)["since"] is null, $"{endpoint}: since should be omitted in {handler.LastRequest.RequestUri}");
    }

    [Fact]
    public async Task ShouldKeepQuantityAlongsideSince()
    {
        var handler = new RecordingHttpMessageHandler("""{ "data": { "metric": "Circuit rating", "unit": "MVA", "circuit_rating": { "timestamp": "2026-01-01T12:00:00Z", "value": 1.0, "is_fallback": false } } }""");

        await HeimdallApiClientFactory.Create(handler).GetLatestCircuitRatingAsync(Id, Quantity.ApparentPower, Since);

        Assert.Equal("apparent_power", QueryString.Of(handler.LastRequest)["quantity"]);
    }
}
