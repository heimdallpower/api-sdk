using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest Heimdall DLR for "Heimdall Power Line" in amperes and in MVA, and checks that the MVA value
/// is the three-phase apparent power of the ampere value at the facility voltage from the asset hierarchy.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestHeimdallDlr(GetLatestHeimdallDlr.Scenario scenario) : IClassFixture<GetLatestHeimdallDlr.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestHeimdallDlrResponse Amperes { get; }
        public LatestHeimdallDlrResponse Mva { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            // Retry so both calls see the same calculation if a new value lands between them.
            for (var attempt = 0; ; attempt++)
            {
                Amperes = Client.GetLatestHeimdallDlrAsync(Line.LineId).GetAwaiter().GetResult();
                Mva = Client.GetLatestHeimdallDlrAsync(Line.LineId, Quantity.ApparentPower).GetAwaiter().GetResult();
                if (Amperes.HeimdallDlr.Timestamp == Mva.HeimdallDlr.Timestamp || attempt == 2)
                    break;
            }
        }
    }

    [Fact]
    public void UnitShouldFollowQuantity()
    {
        Assert.Equal(LineAssets.AmpereUnit, scenario.Amperes.Unit);
        Assert.Equal(LineAssets.MvaUnit, scenario.Mva.Unit);
    }

    [Fact]
    public void MetricShouldNotDependOnQuantity()
    {
        Assert.Equal(scenario.Amperes.Metric, scenario.Mva.Metric);
    }

    [Fact]
    public void ApparentPowerShouldBeThreePhaseConversionOfAmpacity()
    {
        Assert.Equal(scenario.Amperes.HeimdallDlr.Timestamp, scenario.Mva.HeimdallDlr.Timestamp);
        Assert.True(scenario.Mva.HeimdallDlr.Value > 0, $"Apparent power {scenario.Mva.HeimdallDlr.Value} should be positive");
        scenario.Line.AssertIsApparentPowerOf(scenario.Mva.HeimdallDlr.Value, scenario.Amperes.HeimdallDlr.Value, "Latest Heimdall DLR");
    }

    [Fact]
    public void AtSpanIdShouldReferToASpanOnTheLine()
    {
        Assert.Contains(scenario.Amperes.HeimdallDlr.AtSpanId, scenario.Line.SpanIds);
    }

    [Fact]
    public void AtSpanIdShouldNotDependOnQuantity()
    {
        Assert.Equal(scenario.Amperes.HeimdallDlr.AtSpanId, scenario.Mva.HeimdallDlr.AtSpanId);
    }
}
