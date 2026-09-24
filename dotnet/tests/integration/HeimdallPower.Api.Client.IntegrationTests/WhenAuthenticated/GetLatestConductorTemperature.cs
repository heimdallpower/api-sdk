using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries the most recent conductor temperature for "Heimdall Power Line".</summary>
[Trait("Category", "Integration")]
public class GetLatestConductorTemperature(GetLatestConductorTemperature.Scenario scenario) : IClassFixture<GetLatestConductorTemperature.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        private static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public LatestConductorTemperatureResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetLatestConductorTemperatureAsync(HeimdallPowerLineId).GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void ShouldReturnResponse()
    {
        Assert.NotNull(scenario.Result);
    }

    [Fact]
    public void ResultShouldHaveMetric()
    {
        Assert.False(string.IsNullOrEmpty(scenario.Result?.Metric), "Metric should not be empty");
    }

    [Fact]
    public void ResultShouldHaveUnit()
    {
        Assert.False(string.IsNullOrEmpty(scenario.Result?.Unit), "Unit should not be empty");
    }

    [Fact]
    public void MinShouldNotExceedMax_WhenPresent()
    {
        var conductorTemperature = scenario.Result!.ConductorTemperature;
        if (conductorTemperature.Min is { } min)
        {
            Assert.True(min <= conductorTemperature.Max,
                $"Min temperature {min} should not exceed max temperature {conductorTemperature.Max}");
        }
    }

    [Fact]
    public void MeasurementPointTemperaturesShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Result?.MeasurementPointTemperatures);
    }
}

/// <summary>
/// Queries the most recent conductor temperature for "Heimdall Power Line" with
/// <c>include=measurement_points</c> and cross-checks the per-measurement-point breakdown
/// against the real asset hierarchy returned by <see cref="HeimdallApiClient.GetAssetsAsync"/>.
/// </summary>
[Trait("Category", "Integration")]
public class GetLatestConductorTemperatureWithMeasurementPoints(
    GetLatestConductorTemperatureWithMeasurementPoints.Scenario scenario)
    : IClassFixture<GetLatestConductorTemperatureWithMeasurementPoints.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        public static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public LatestConductorTemperatureResponse? Result { get; }
        public AssetsResponse Assets { get; }

        public Scenario()
        {
            Result = Client.GetLatestConductorTemperatureAsync(HeimdallPowerLineId, include: ConductorTemperatureInclude.MeasurementPoints)
                .GetAwaiter().GetResult();
            Assets = Client.GetAssetsAsync().GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void MeasurementPointTemperaturesShouldNotBeNull_WhenRequested()
    {
        // The underlying list may be empty if no recent data exists – that's valid.
        // Only the presence of the field itself (honoring `include`) is guaranteed.
        Assert.NotNull(scenario.Result?.MeasurementPointTemperatures);
    }

    [Fact]
    public void AllSpanPhaseAndMeasurementPointIdsShouldExistInAssets()
    {
        var line = scenario.Assets.AllLines().SingleOrDefault(l => l?.Id == Scenario.HeimdallPowerLineId);
        Assert.NotNull(line);

        var knownSpanIds = line!.Spans.Select(s => s.Id).ToHashSet();
        var knownSpanPhaseIds = line.Spans.SelectMany(s => s.SpanPhases).Select(sp => sp.Id).ToHashSet();
        var knownMeasurementPointIds = line.Spans
            .SelectMany(s => s.SpanPhases)
            .SelectMany(sp => sp.MeasurementPoints)
            .Select(mp => mp.Id)
            .ToHashSet();

        var spans = scenario.Result!.MeasurementPointTemperatures!;
        Assert.All(spans, span =>
        {
            Assert.Contains(span.SpanId, knownSpanIds);
            Assert.All(span.SpanPhases, spanPhase =>
            {
                Assert.Contains(spanPhase.SpanPhaseId, knownSpanPhaseIds);
                Assert.All(spanPhase.MeasurementPoints, measurementPoint =>
                    Assert.Contains(measurementPoint.MeasurementPointId, knownMeasurementPointIds));
            });
        });
    }
}
