using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest and last six hours of current and apparent power for "Heimdall Power Line" and checks that
/// <c>at_span_id</c> refers to a span on the line, and that apparent power, derived from the line current,
/// points at the same span as the current at the same timestamp.
/// </summary>
[Trait("Category", "Integration")]
public class CurrentAtSpanId(CurrentAtSpanId.Scenario scenario) : IClassFixture<CurrentAtSpanId.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestCurrentResponse LatestCurrent { get; }
        public LatestApparentPowerResponse LatestApparentPower { get; }
        public CurrentsResponse Currents { get; }
        public ApparentPowersResponse ApparentPowers { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);
            var to = DateTimeOffset.UtcNow;
            var from = to.AddHours(-6);

            // Retry so both latest calls see the same measurement if a new value lands between them.
            for (var attempt = 0; ; attempt++)
            {
                LatestCurrent = Client.GetLatestCurrentAsync(Line.LineId).GetAwaiter().GetResult();
                LatestApparentPower = Client.GetLatestApparentPowerAsync(Line.LineId).GetAwaiter().GetResult();
                if (LatestCurrent.Current.Timestamp == LatestApparentPower.ApparentPower.Timestamp || attempt == 2)
                    break;
            }

            Currents = Client.GetCurrentsAsync(Line.LineId, from, to).GetAwaiter().GetResult();
            ApparentPowers = Client.GetApparentPowersAsync(Line.LineId, from, to).GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void LatestAtSpanIdsShouldReferToSpansOnTheLine()
    {
        Assert.Contains(scenario.LatestCurrent.Current.AtSpanId, scenario.Line.SpanIds);
        Assert.Contains(scenario.LatestApparentPower.ApparentPower.AtSpanId, scenario.Line.SpanIds);
    }

    [Fact]
    public void HistoricalAtSpanIdsShouldReferToSpansOnTheLine()
    {
        Assert.All(scenario.Currents.Currents, current => Assert.Contains(current.AtSpanId, scenario.Line.SpanIds));
        Assert.All(scenario.ApparentPowers.ApparentPowers, apparentPower => Assert.Contains(apparentPower.AtSpanId, scenario.Line.SpanIds));
    }

    [Fact]
    public void ApparentPowerShouldPointAtTheSameSpanAsTheCurrentItIsDerivedFrom()
    {
        if (scenario.LatestCurrent.Current.Timestamp == scenario.LatestApparentPower.ApparentPower.Timestamp)
            Assert.Equal(scenario.LatestCurrent.Current.AtSpanId, scenario.LatestApparentPower.ApparentPower.AtSpanId);

        var currentSpans = scenario.Currents.Currents.ToDictionary(current => current.Timestamp, current => current.AtSpanId);
        Assert.All(scenario.ApparentPowers.ApparentPowers.Where(apparentPower => currentSpans.ContainsKey(apparentPower.Timestamp)),
            apparentPower => Assert.Equal(currentSpans[apparentPower.Timestamp], apparentPower.AtSpanId));
    }
}
