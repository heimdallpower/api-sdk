using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest circuit rating for the facility on "Heimdall Power Line" in amperes and in MVA, and checks that
/// the MVA value is the three-phase apparent power of the ampere value at the facility voltage from the asset hierarchy.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestCircuitRating(GetLatestCircuitRating.Scenario scenario) : IClassFixture<GetLatestCircuitRating.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestCircuitRatingResponse Amperes { get; }
        public LatestCircuitRatingResponse Mva { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            // Retry so both calls see the same calculation if a new value lands between them.
            for (var attempt = 0; ; attempt++)
            {
                Amperes = Client.GetLatestCircuitRatingAsync(Line.FacilityId).GetAwaiter().GetResult();
                Mva = Client.GetLatestCircuitRatingAsync(Line.FacilityId, Quantity.ApparentPower).GetAwaiter().GetResult();
                if (Amperes.CircuitRating.Timestamp == Mva.CircuitRating.Timestamp || attempt == 2)
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
    public void ApparentPowerShouldBeThreePhaseConversionOfRating()
    {
        Assert.Equal(scenario.Amperes.CircuitRating.Timestamp, scenario.Mva.CircuitRating.Timestamp);
        Assert.True(scenario.Mva.CircuitRating.Value > 0, $"Apparent power {scenario.Mva.CircuitRating.Value} should be positive");
        scenario.Line.AssertIsApparentPowerOf(scenario.Mva.CircuitRating.Value, scenario.Amperes.CircuitRating.Value, "Latest circuit rating");
    }

    [Fact]
    public void LimitingComponentShouldNotDependOnQuantity()
    {
        Assert.Equal(scenario.Amperes.CircuitRating.AtFacilityComponentId, scenario.Mva.CircuitRating.AtFacilityComponentId);
    }
}
