using System.Net;
using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.UnitTests.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenRequestingWithOptions;

/// <summary>
/// Every data endpoint takes an optional options record. Passing <c>null</c> must behave exactly like passing
/// a default-constructed record, and both must send the documented defaults (<c>quantity=current</c>,
/// <c>unit_system=metric</c>) and nothing else. The fake transport answers 404, so only the request is inspected.
/// </summary>
[Trait("Category", "Unit")]
public class DefaultOptions
{
    private static readonly Guid Id = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To = From.AddDays(1);

    private const string DefaultQuantity = "quantity=current";
    private const string DefaultUnitSystem = "unit_system=metric";

    /// <summary>Endpoint name, expected default query (besides the time range), and a call taking "use null options".</summary>
    public static TheoryData<string, string[], Func<HeimdallApiClient, bool, Task>> Endpoints => new()
    {
        { "latest current", [], (c, n) => c.GetLatestCurrentAsync(Id, n ? null : new()) },
        { "latest conductor temperature", [DefaultUnitSystem], (c, n) => c.GetLatestConductorTemperatureAsync(Id, n ? null : new()) },
        { "latest icing", [DefaultUnitSystem], (c, n) => c.GetLatestIcingAsync(Id, n ? null : new()) },
        { "latest sag and clearance", [DefaultUnitSystem], (c, n) => c.GetLatestSagAndClearanceAsync(Id, n ? null : new()) },
        { "sag and clearances", [DefaultUnitSystem], (c, n) => c.GetSagAndClearancesAsync(Id, From, To, n ? null : new()) },
        { "icings", [DefaultUnitSystem], (c, n) => c.GetIcingsAsync(Id, From, To, n ? null : new()) },
        { "icing forecast", [DefaultUnitSystem], (c, n) => c.GetIcingForecastAsync(Id, n ? null : new()) },
        { "latest apparent power", [], (c, n) => c.GetLatestApparentPowerAsync(Id, n ? null : new()) },
        { "apparent powers", [], (c, n) => c.GetApparentPowersAsync(Id, From, To, n ? null : new()) },
        { "currents", [], (c, n) => c.GetCurrentsAsync(Id, From, To, n ? null : new()) },
        { "conductor temperatures", [DefaultUnitSystem], (c, n) => c.GetConductorTemperaturesAsync(Id, From, To, n ? null : new()) },
        { "latest Heimdall DLR", [DefaultQuantity], (c, n) => c.GetLatestHeimdallDlrAsync(Id, n ? null : new()) },
        { "latest Heimdall AAR", [DefaultQuantity], (c, n) => c.GetLatestHeimdallAarAsync(Id, n ? null : new()) },
        { "latest line transient rating", [DefaultQuantity], (c, n) => c.GetLatestLineTransientRatingAsync(Id, n ? null : new()) },
        { "Heimdall DLR forecasts", [DefaultQuantity], (c, n) => c.GetHeimdallDlrForecastsAsync(Id, n ? null : new()) },
        { "Heimdall AAR forecasts", [DefaultQuantity], (c, n) => c.GetHeimdallAarForecastsAsync(Id, n ? null : new()) },
        { "Heimdall DLRs", [DefaultQuantity], (c, n) => c.GetHeimdallDlrsAsync(Id, From, To, n ? null : new()) },
        { "Heimdall AARs", [DefaultQuantity], (c, n) => c.GetHeimdallAarsAsync(Id, From, To, n ? null : new()) },
        { "circuit rating forecasts", [DefaultQuantity], (c, n) => c.GetCircuitRatingForecastsAsync(Id, n ? null : new()) },
        { "latest circuit rating", [DefaultQuantity], (c, n) => c.GetLatestCircuitRatingAsync(Id, n ? null : new()) },
        { "circuit ratings", [DefaultQuantity], (c, n) => c.GetCircuitRatingsAsync(Id, From, To, n ? null : new()) },
        { "latest circuit transient rating", [DefaultQuantity], (c, n) => c.GetLatestCircuitTransientRatingAsync(Id, n ? null : new()) },
    };

    [Theory]
    [MemberData(nameof(Endpoints))]
    public async Task ShouldSendOnlyDocumentedDefaults_WhenOptionsAreNullOrDefault(string endpoint, string[] expectedDefaults, Func<HeimdallApiClient, bool, Task> call)
    {
        var withNull = await RequestOf(client => call(client, true));
        var withDefault = await RequestOf(client => call(client, false));

        var query = QueryString.Of(withNull);
        var sent = query.AllKeys
            .Where(key => key is not ("from_timestamp" or "to_timestamp"))
            .Select(key => $"{key}={query[key]}")
            .Order();

        Assert.Equal(withDefault.RequestUri, withNull.RequestUri);
        Assert.True(expectedDefaults.Order().SequenceEqual(sent), $"{endpoint}: unexpected query in {withNull.RequestUri}");
    }

    [Fact]
    public async Task ShouldSendImperial_WhenUnitSystemIsImperial()
    {
        var request = await RequestOf(client => client.GetIcingsAsync(Id, From, To, new() { UnitSystem = UnitSystem.Imperial }));

        Assert.Equal("imperial", QueryString.Of(request)["unit_system"]);
    }

    [Fact]
    public async Task ShouldSendApparentPower_WhenQuantityIsApparentPower()
    {
        var request = await RequestOf(client => client.GetHeimdallDlrForecastsAsync(Id, new() { Quantity = Quantity.ApparentPower }));

        Assert.Equal("apparent_power", QueryString.Of(request)["quantity"]);
    }

    private static async Task<HttpRequestMessage> RequestOf(Func<HeimdallApiClient, Task> call)
    {
        var handler = new RecordingHttpMessageHandler("", HttpStatusCode.NotFound);

        await Assert.ThrowsAsync<HeimdallApiException>(() => call(HeimdallApiClientFactory.Create(handler)));

        return handler.LastRequest;
    }
}
