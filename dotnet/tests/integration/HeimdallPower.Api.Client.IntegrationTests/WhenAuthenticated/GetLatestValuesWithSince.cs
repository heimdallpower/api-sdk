using System.Net;
using HeimdallPower.Api.Client.CapacityMonitoring;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest current, apparent power, Heimdall DLR, Heimdall AAR and circuit rating for
/// "Heimdall Power Line" with a <c>since</c> one day back: every returned value must be at or after <c>since</c>.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestValuesWithSince(GetLatestValuesWithSince.Scenario scenario) : IClassFixture<GetLatestValuesWithSince.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public DateTimeOffset Since { get; } = DateTimeOffset.UtcNow.AddDays(-1);
        public DateTimeOffset CurrentTimestamp { get; }
        public DateTimeOffset ApparentPowerTimestamp { get; }
        public DateTimeOffset HeimdallDlrTimestamp { get; }
        public DateTimeOffset HeimdallAarTimestamp { get; }
        public DateTimeOffset CircuitRatingTimestamp { get; }

        public Scenario()
        {
            var line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            CurrentTimestamp = Client.GetLatestCurrentAsync(line.LineId, Since).GetAwaiter().GetResult().Current.Timestamp;
            ApparentPowerTimestamp = Client.GetLatestApparentPowerAsync(line.LineId, Since).GetAwaiter().GetResult().ApparentPower.Timestamp;
            HeimdallDlrTimestamp = Client.GetLatestHeimdallDlrAsync(line.LineId, since: Since).GetAwaiter().GetResult().HeimdallDlr.Timestamp;
            HeimdallAarTimestamp = Client.GetLatestHeimdallAarAsync(line.LineId, since: Since).GetAwaiter().GetResult().HeimdallAar.Timestamp;
            CircuitRatingTimestamp = Client.GetLatestCircuitRatingAsync(line.FacilityId, since: Since).GetAwaiter().GetResult().CircuitRating.Timestamp;
        }
    }

    [Fact]
    public void LatestCurrentShouldBeAtOrAfterSince() => AssertAtOrAfterSince(scenario.CurrentTimestamp);

    [Fact]
    public void LatestApparentPowerShouldBeAtOrAfterSince() => AssertAtOrAfterSince(scenario.ApparentPowerTimestamp);

    [Fact]
    public void LatestHeimdallDlrShouldBeAtOrAfterSince() => AssertAtOrAfterSince(scenario.HeimdallDlrTimestamp);

    [Fact]
    public void LatestHeimdallAarShouldBeAtOrAfterSince() => AssertAtOrAfterSince(scenario.HeimdallAarTimestamp);

    [Fact]
    public void LatestCircuitRatingShouldBeAtOrAfterSince() => AssertAtOrAfterSince(scenario.CircuitRatingTimestamp);

    private void AssertAtOrAfterSince(DateTimeOffset timestamp) =>
        Assert.True(timestamp >= scenario.Since, $"Timestamp {timestamp:O} is before since {scenario.Since:O}");
}

/// <summary>
/// Queries the same latest endpoints with a <c>since</c> in the future. No value can be that new, so each must report
/// 404 (no data) rather than return a stale value; a 200 here means <c>since</c> was not sent.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestValuesWithFutureSince(GetLatestValuesWithFutureSince.Scenario scenario) : IClassFixture<GetLatestValuesWithFutureSince.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        private static readonly DateTimeOffset Since = DateTimeOffset.UtcNow.AddHours(1);

        public HttpStatusCode? Current { get; }
        public HttpStatusCode? ApparentPower { get; }
        public HttpStatusCode? HeimdallDlr { get; }
        public HttpStatusCode? HeimdallAar { get; }
        public HttpStatusCode? CircuitRating { get; }

        public Scenario()
        {
            var line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            Current = StatusOf(() => Client.GetLatestCurrentAsync(line.LineId, Since));
            ApparentPower = StatusOf(() => Client.GetLatestApparentPowerAsync(line.LineId, Since));
            HeimdallDlr = StatusOf(() => Client.GetLatestHeimdallDlrAsync(line.LineId, Quantity.Current, Since));
            HeimdallAar = StatusOf(() => Client.GetLatestHeimdallAarAsync(line.LineId, Quantity.Current, Since));
            CircuitRating = StatusOf(() => Client.GetLatestCircuitRatingAsync(line.FacilityId, Quantity.Current, Since));
        }

        /// <summary>The error status of the call, or null when it succeeded.</summary>
        private static HttpStatusCode? StatusOf(Func<Task> call)
        {
            try
            {
                call().GetAwaiter().GetResult();
                return null;
            }
            catch (HeimdallApiException e)
            {
                return e.StatusCode;
            }
        }
    }

    [Fact]
    public void LatestCurrentShouldReportNoData() => Assert.Equal(HttpStatusCode.NotFound, scenario.Current);

    [Fact]
    public void LatestApparentPowerShouldReportNoData() => Assert.Equal(HttpStatusCode.NotFound, scenario.ApparentPower);

    [Fact]
    public void LatestHeimdallDlrShouldReportNoData() => Assert.Equal(HttpStatusCode.NotFound, scenario.HeimdallDlr);

    [Fact]
    public void LatestHeimdallAarShouldReportNoData() => Assert.Equal(HttpStatusCode.NotFound, scenario.HeimdallAar);

    [Fact]
    public void LatestCircuitRatingShouldReportNoData() => Assert.Equal(HttpStatusCode.NotFound, scenario.CircuitRating);
}
