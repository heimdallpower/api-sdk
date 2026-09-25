using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest Heimdall AAR for "Heimdall Power Line" in amperes and in MVA, and checks that the MVA value
/// is the three-phase apparent power of the ampere value at the facility voltage from the asset hierarchy.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestHeimdallAar(GetLatestHeimdallAar.Scenario scenario) : IClassFixture<GetLatestHeimdallAar.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestHeimdallAarResponse Amperes { get; }
        public LatestHeimdallAarResponse Mva { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            // Retry so both calls see the same calculation if a new value lands between them.
            for (var attempt = 0; ; attempt++)
            {
                Amperes = Client.GetLatestHeimdallAarAsync(Line.LineId).GetAwaiter().GetResult();
                Mva = Client.GetLatestHeimdallAarAsync(Line.LineId, Quantity.ApparentPower).GetAwaiter().GetResult();
                if (Amperes.HeimdallAar.Timestamp == Mva.HeimdallAar.Timestamp || attempt == 2)
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
        Assert.Equal(scenario.Amperes.HeimdallAar.Timestamp, scenario.Mva.HeimdallAar.Timestamp);
        Assert.True(scenario.Mva.HeimdallAar.Value > 0, $"Apparent power {scenario.Mva.HeimdallAar.Value} should be positive");
        scenario.Line.AssertIsApparentPowerOf(scenario.Mva.HeimdallAar.Value, scenario.Amperes.HeimdallAar.Value, "Latest Heimdall AAR");
    }
}
