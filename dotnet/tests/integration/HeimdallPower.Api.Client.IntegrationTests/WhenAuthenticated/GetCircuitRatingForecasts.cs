using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest circuit rating forecasts for the facility on "Heimdall Power Line" in amperes and in MVA, and
/// checks that every MVA percentile is the three-phase apparent power of the matching ampere percentile.
/// </summary>
[Trait("Category", "Integration")]
public class GetCircuitRatingForecasts(GetCircuitRatingForecasts.Scenario scenario) : IClassFixture<GetCircuitRatingForecasts.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public CircuitRatingForecastResponse Amperes { get; }
        public CircuitRatingForecastResponse Mva { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            // Retry so both calls see the same forecast run if a new one lands between them.
            for (var attempt = 0; ; attempt++)
            {
                Amperes = Client.GetCircuitRatingForecastsAsync(Line.FacilityId).GetAwaiter().GetResult();
                Mva = Client.GetCircuitRatingForecastsAsync(Line.FacilityId, Quantity.ApparentPower).GetAwaiter().GetResult();
                if (Amperes.UpdatedTimestamp == Mva.UpdatedTimestamp || attempt == 2)
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
    public void ApparentPowerForecastsShouldBeThreePhaseConversionOfRatingForecasts()
    {
        Assert.Equal(scenario.Amperes.UpdatedTimestamp, scenario.Mva.UpdatedTimestamp);
        ForecastAssertions.AssertApparentPowerOf(scenario.Mva.CircuitRatingForecasts, scenario.Amperes.CircuitRatingForecasts, scenario.Line);
    }
}
