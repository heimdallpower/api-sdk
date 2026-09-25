using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>
/// Queries the latest Heimdall DLR forecasts for "Heimdall Power Line" in amperes and in MVA, and checks that every
/// MVA percentile is the three-phase apparent power of the matching ampere percentile.
/// </summary>
[Trait("Category", "Integration")]
public class GetHeimdallDlrForecasts(GetHeimdallDlrForecasts.Scenario scenario) : IClassFixture<GetHeimdallDlrForecasts.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public HeimdallDlrForecastResponse Amperes { get; }
        public HeimdallDlrForecastResponse Mva { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);

            // Retry so both calls see the same forecast run if a new one lands between them.
            for (var attempt = 0; ; attempt++)
            {
                Amperes = Client.GetHeimdallDlrForecastsAsync(Line.LineId).GetAwaiter().GetResult();
                Mva = Client.GetHeimdallDlrForecastsAsync(Line.LineId, Quantity.ApparentPower).GetAwaiter().GetResult();
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
        ForecastAssertions.AssertApparentPowerOf(scenario.Mva.HeimdallDlrForecasts, scenario.Amperes.HeimdallDlrForecasts, scenario.Line);
    }

    [Fact]
    public void AllAtSpanIdsShouldReferToSpansOnTheLine()
    {
        ForecastAssertions.AssertAtSpanIdsOnLine(scenario.Amperes.HeimdallDlrForecasts, scenario.Line);
        ForecastAssertions.AssertAtSpanIdsOnLine(scenario.Mva.HeimdallDlrForecasts, scenario.Line);
    }
}
