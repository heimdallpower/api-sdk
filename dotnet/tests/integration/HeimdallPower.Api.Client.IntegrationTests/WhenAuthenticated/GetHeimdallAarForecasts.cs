using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest Heimdall AAR forecasts for "Heimdall Power Line" in amperes and in MVA, and checks that every
/// MVA percentile is the three-phase apparent power of the matching ampere percentile.
/// </summary>
[Trait("Category", "Integration")]
public class GetHeimdallAarForecasts(GetHeimdallAarForecasts.Scenario scenario) : IClassFixture<GetHeimdallAarForecasts.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public HeimdallAarForecastResponse Amperes { get; }
        public HeimdallAarForecastResponse Mva { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            // Retry so both calls see the same forecast run if a new one lands between them.
            for (var attempt = 0; ; attempt++)
            {
                Amperes = Client.GetHeimdallAarForecastsAsync(Line.LineId).GetAwaiter().GetResult();
                Mva = Client.GetHeimdallAarForecastsAsync(Line.LineId, Quantity.ApparentPower).GetAwaiter().GetResult();
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
    public void ApparentPowerForecastsShouldBeThreePhaseConversionOfAmpacityForecasts()
    {
        Assert.Equal(scenario.Amperes.UpdatedTimestamp, scenario.Mva.UpdatedTimestamp);
        ForecastAssertions.AssertApparentPowerOf(scenario.Mva.HeimdallAarForecasts, scenario.Amperes.HeimdallAarForecasts, scenario.Line);
    }

    [Fact]
    public void AllAtSpanIdsShouldReferToSpansOnTheLine()
    {
        ForecastAssertions.AssertAtSpanIdsOnLine(scenario.Amperes.HeimdallAarForecasts, scenario.Line);
        ForecastAssertions.AssertAtSpanIdsOnLine(scenario.Mva.HeimdallAarForecasts, scenario.Line);
    }
}
