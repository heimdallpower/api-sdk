using HeimdallPower.Api.Client.GridInsights.Lines;
using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries historical current data for "Heimdall Power Line" (2026-01-01).</summary>
[Trait("Category", "Integration")]
public class GetCurrents(GetCurrents.Scenario scenario) : IClassFixture<GetCurrents.Scenario>
{
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To   = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        private static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public CurrentsResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetCurrentsAsync(HeimdallPowerLineId, From, To).GetAwaiter().GetResult();
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
    public void ResultShouldHaveCurrentsList()
    {
        // The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
        Assert.NotNull(scenario.Result?.Currents);
    }

    [Fact]
    public void AllCurrentsShouldHaveTimestampsWithinRequestedRange()
    {
        Assert.All(scenario.Result!.Currents, c =>
        {
            Assert.True(c.Timestamp >= From, $"Timestamp {c.Timestamp} is before {From}");
            Assert.True(c.Timestamp <= To,   $"Timestamp {c.Timestamp} is after {To}");
        });
    }

    [Fact]
    public void MeasurementPointCurrentsShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Result?.MeasurementPointCurrents);
    }
}

/// <summary>
/// Queries the last six hours of current for "Heimdall Power Line" with <c>include=measurement_points</c>
/// and cross-checks the per-measurement-point breakdown against the asset hierarchy and the requested window.
/// </summary>
[Trait("Category", "Integration")]
public class GetCurrentsWithMeasurementPoints(GetCurrentsWithMeasurementPoints.Scenario scenario)
    : IClassFixture<GetCurrentsWithMeasurementPoints.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public DateTimeOffset From { get; }
        public DateTimeOffset To { get; }
        public CurrentsResponse Result { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            To = DateTimeOffset.UtcNow;
            From = To.AddHours(-6);
            Result = Client.GetCurrentsAsync(LineAssets.HeimdallPowerLineId, From, To, CurrentInclude.MeasurementPoints)
                .GetAwaiter().GetResult();
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);
        }
    }

    private IEnumerable<MeasurementPointCurrentDto> MeasurementPoints =>
        scenario.Result.MeasurementPointCurrents!.SelectMany(s => s.SpanPhases).SelectMany(sp => sp.MeasurementPoints);

    [Fact]
    public void MeasurementPointCurrentsShouldHaveReadings_WhenTheLineHasCurrents()
    {
        // The line-level series is derived from the measurement points, so readings on the line imply readings per measurement point.
        if (scenario.Result.Currents.Count > 0)
            Assert.Contains(MeasurementPoints, mp => mp.Currents.Count > 0);
    }

    [Fact]
    public void MeasurementPointCurrentsShouldBePresentWithIdsFromAssets_WhenRequested()
    {
        // The list may be empty when the window has no data; only its presence (honoring `include`) is guaranteed.
        Assert.NotNull(scenario.Result.MeasurementPointCurrents);
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
    public void AllMeasurementPointReadingsShouldBeNonNegativeAndWithinRequestedRange()
    {
        Assert.All(MeasurementPoints.SelectMany(mp => mp.Currents), reading =>
        {
            Assert.True(reading.Value >= 0, $"Current {reading.Value} at {reading.Timestamp} should not be negative");
            Assert.Equal(TimeSpan.Zero, reading.Timestamp.Offset);
            Assert.True(reading.Timestamp >= scenario.From, $"Timestamp {reading.Timestamp} is before {scenario.From}");
            Assert.True(reading.Timestamp <= scenario.To, $"Timestamp {reading.Timestamp} is after {scenario.To}");
        });
    }
}

