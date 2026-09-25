using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries the most recent current for "Heimdall Power Line" without <c>include</c>.</summary>
[Trait("Category", "Integration")]
public class GetLatestCurrent(GetLatestCurrent.Scenario scenario) : IClassFixture<GetLatestCurrent.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestCurrentResponse Result { get; }

        public Scenario()
        {
            Result = Client.GetLatestCurrentAsync(LineAssets.HeimdallPowerLineId).GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void ResultShouldBeInAmperes()
    {
        Assert.Equal(LineAssets.AmpereUnit, scenario.Result.Unit);
    }

    [Fact]
    public void CurrentShouldBeNonNegativeWithUtcTimestamp()
    {
        Assert.True(scenario.Result.Current.Value >= 0, $"Current {scenario.Result.Current.Value} should not be negative");
        Assert.Equal(TimeSpan.Zero, scenario.Result.Current.Timestamp.Offset);
    }

    [Fact]
    public void MeasurementPointCurrentsShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Result.MeasurementPointCurrents);
    }
}

/// <summary>
/// Queries the most recent current for "Heimdall Power Line" with <c>include=measurement_points</c>
/// and cross-checks the per-measurement-point breakdown against the asset hierarchy.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestCurrentWithMeasurementPoints(GetLatestCurrentWithMeasurementPoints.Scenario scenario)
    : IClassFixture<GetLatestCurrentWithMeasurementPoints.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public LatestCurrentResponse Result { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            Result = Client.GetLatestCurrentAsync(LineAssets.HeimdallPowerLineId, include: CurrentInclude.MeasurementPoints)
                .GetAwaiter().GetResult();
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);
        }
    }

    [Fact]
    public void MeasurementPointCurrentsShouldBePopulatedWithIdsFromAssets_WhenRequested()
    {
        // A latest line current exists (the call returned 200), so at least one measurement point measured it.
        Assert.NotNull(scenario.Result.MeasurementPointCurrents);
        Assert.NotEmpty(scenario.Result.MeasurementPointCurrents!.SelectMany(s => s.SpanPhases).SelectMany(sp => sp.MeasurementPoints));

        Assert.All(scenario.Result.MeasurementPointCurrents!, span =>
        {
            Assert.Contains(span.SpanId, scenario.Line.SpanIds);
            Assert.All(span.SpanPhases, spanPhase =>
            {
                Assert.Contains(spanPhase.SpanPhaseId, scenario.Line.SpanPhaseIds);
                Assert.All(spanPhase.MeasurementPoints, mp => Assert.Contains(mp.MeasurementPointId, scenario.Line.MeasurementPointIds));
            });
        });
    }

    [Fact]
    public void AllMeasurementPointCurrentsShouldBeNonNegativeWithUtcTimestamps()
    {
        var measurementPoints = scenario.Result.MeasurementPointCurrents!
            .SelectMany(s => s.SpanPhases)
            .SelectMany(sp => sp.MeasurementPoints);

        Assert.All(measurementPoints, mp =>
        {
            Assert.True(mp.Value >= 0, $"Current {mp.Value} at measurement point {mp.MeasurementPointId} should not be negative");
            Assert.Equal(TimeSpan.Zero, mp.Timestamp.Offset);
        });
    }
}
