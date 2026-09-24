using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries historical conductor temperature data for "Heimdall Power Line" (2026-01-01).</summary>
[Trait("Category", "Integration")]
public class GetConductorTemperatures(GetConductorTemperatures.Scenario scenario) : IClassFixture<GetConductorTemperatures.Scenario>
{
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To   = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        private static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public ConductorTemperaturesResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetConductorTemperaturesAsync(HeimdallPowerLineId, From, To).GetAwaiter().GetResult();
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
    public void ResultShouldHaveConductorTemperaturesList()
    {
        // The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
        Assert.NotNull(scenario.Result?.ConductorTemperatures);
    }

    [Fact]
    public void AllReadingsShouldHaveTimestampsWithinRequestedRange()
    {
        Assert.All(scenario.Result!.ConductorTemperatures, ct =>
        {
            Assert.True(ct.Timestamp >= From, $"Timestamp {ct.Timestamp} is before {From}");
            Assert.True(ct.Timestamp <= To,   $"Timestamp {ct.Timestamp} is after {To}");
        });
    }

    [Fact]
    public void MeasurementPointTemperaturesShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Result?.MeasurementPointTemperatures);
    }
}

/// <summary>
/// Queries historical conductor temperature data for "Heimdall Power Line" with
/// <c>include=measurement_points</c> and cross-checks the per-measurement-point breakdown
/// against the real asset hierarchy returned by <see cref="HeimdallApiClient.GetAssetsAsync"/>.
/// </summary>
[Trait("Category", "Integration")]
public class GetConductorTemperaturesWithMeasurementPoints(
    GetConductorTemperaturesWithMeasurementPoints.Scenario scenario)
    : IClassFixture<GetConductorTemperaturesWithMeasurementPoints.Scenario>
{
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To   = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        public static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public ConductorTemperaturesResponse? Result { get; }
        public AssetsResponse Assets { get; }

        public Scenario()
        {
            Result = Client.GetConductorTemperaturesAsync(HeimdallPowerLineId, From, To, include: ConductorTemperatureInclude.MeasurementPoints)
                .GetAwaiter().GetResult();
            Assets = Client.GetAssetsAsync().GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void MeasurementPointTemperaturesShouldNotBeNull_WhenRequested()
    {
        // The underlying list may be empty if no data exists for the period – that's valid.
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

    [Fact]
    public void AllMeasurementPointReadingsShouldHaveTimestampsWithinRequestedRange()
    {
        var measurementPoints = scenario.Result!.MeasurementPointTemperatures!
            .SelectMany(span => span.SpanPhases)
            .SelectMany(spanPhase => spanPhase.MeasurementPoints);

        Assert.All(measurementPoints, measurementPoint =>
            Assert.All(measurementPoint.Temperatures, dataPoint =>
            {
                Assert.True(dataPoint.Timestamp >= From, $"Timestamp {dataPoint.Timestamp} is before {From}");
                Assert.True(dataPoint.Timestamp <= To,   $"Timestamp {dataPoint.Timestamp} is after {To}");
            }));
    }
}
