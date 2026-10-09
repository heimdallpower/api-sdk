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
                Mva = Client.GetLatestHeimdallDlrAsync(Line.LineId, new() { Quantity = Quantity.ApparentPower }).GetAwaiter().GetResult();
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

    [Fact]
    public void HeimdallSpanDlrsShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Amperes.HeimdallSpanDlrs);
    }
}

/// <summary>
/// Queries the latest Heimdall DLR for "Heimdall Power Line" with <c>include=spans</c> and cross-checks the
/// per-span breakdown against the asset hierarchy and the line-level timestamp.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestHeimdallDlrWithSpans(GetLatestHeimdallDlrWithSpans.Scenario scenario)
    : IClassFixture<GetLatestHeimdallDlrWithSpans.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestHeimdallDlrResponse Result { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);
            Result = Client.GetLatestHeimdallDlrAsync(Line.LineId, new() { Include = HeimdallDlrInclude.Spans }).GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void HeimdallSpanDlrsShouldBePresentWithSpanIdsFromAssets_WhenRequested()
    {
        // The list may be empty: per-span values are only persisted by the fallback-enabled calculation path.
        Assert.NotNull(scenario.Result.HeimdallSpanDlrs);
        Assert.All(scenario.Result.HeimdallSpanDlrs!, span => Assert.Contains(span.SpanId, scenario.Line.SpanIds));
    }

    [Fact]
    public void HeimdallSpanDlrsShouldBeCalculatedAtTheLineTimestampWithPositiveValues()
    {
        Assert.All(scenario.Result.HeimdallSpanDlrs!, span =>
        {
            Assert.Equal(scenario.Result.HeimdallDlr.Timestamp, span.HeimdallDlr.Timestamp);
            Assert.True(span.HeimdallDlr.Value > 0, $"Span DLR {span.HeimdallDlr.Value} on span {span.SpanId} should be positive");
        });
    }

    [Fact]
    public void HeimdallSpanDlrsShouldListEachSpanOnce()
    {
        var spanIds = scenario.Result.HeimdallSpanDlrs!.Select(span => span.SpanId).ToList();
        Assert.Equal(spanIds.Count, spanIds.Distinct().Count());
    }
}
