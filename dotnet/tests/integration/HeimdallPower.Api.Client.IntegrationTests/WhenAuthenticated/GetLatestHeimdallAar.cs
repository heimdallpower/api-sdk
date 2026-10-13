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
                Mva = Client.GetLatestHeimdallAarAsync(Line.LineId, new() { Quantity = Quantity.ApparentPower }).GetAwaiter().GetResult();
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

    [Fact]
    public void AtSpanIdShouldReferToASpanOnTheLine()
    {
        Assert.Contains(scenario.Amperes.HeimdallAar.AtSpanId, scenario.Line.SpanIds);
    }

    [Fact]
    public void AtSpanIdShouldNotDependOnQuantity()
    {
        Assert.Equal(scenario.Amperes.HeimdallAar.AtSpanId, scenario.Mva.HeimdallAar.AtSpanId);
    }

    [Fact]
    public void HeimdallSpanAarsShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Amperes.HeimdallSpanAars);
    }
}

/// <summary>
/// Queries the latest Heimdall AAR for "Heimdall Power Line" with <c>include=spans</c> and cross-checks the
/// per-span breakdown against the asset hierarchy and the line-level timestamp.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestHeimdallAarWithSpans(GetLatestHeimdallAarWithSpans.Scenario scenario)
    : IClassFixture<GetLatestHeimdallAarWithSpans.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestHeimdallAarResponse Result { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);
            Result = Client.GetLatestHeimdallAarAsync(Line.LineId, new() { Include = HeimdallAarInclude.Spans }).GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void HeimdallSpanAarsShouldBePresentWithSpanIdsFromAssets_WhenRequested()
    {
        // The list may be empty: spans without a Heimdall AAR at the line timestamp are omitted.
        Assert.NotNull(scenario.Result.HeimdallSpanAars);
        Assert.All(scenario.Result.HeimdallSpanAars!, span => Assert.Contains(span.SpanId, scenario.Line.SpanIds));
    }

    [Fact]
    public void HeimdallSpanAarsShouldBeCalculatedAtTheLineTimestampWithPositiveValues()
    {
        Assert.All(scenario.Result.HeimdallSpanAars!, span =>
        {
            Assert.Equal(scenario.Result.HeimdallAar.Timestamp, span.HeimdallAar.Timestamp);
            Assert.True(span.HeimdallAar.Value > 0, $"Span AAR {span.HeimdallAar.Value} on span {span.SpanId} should be positive");
        });
    }

    [Fact]
    public void HeimdallSpanAarsShouldListEachSpanOnce()
    {
        var spanIds = scenario.Result.HeimdallSpanAars!.Select(span => span.SpanId).ToList();
        Assert.Equal(spanIds.Count, spanIds.Distinct().Count());
    }
}
