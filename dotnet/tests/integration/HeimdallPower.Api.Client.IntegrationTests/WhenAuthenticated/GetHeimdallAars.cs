using HeimdallPower.Api.Client.CapacityMonitoring.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries historical Heimdall AAR values for "Heimdall Power Line" (2026-01-01).</summary>
[Trait("Category", "Integration")]
public class GetHeimdallAars(GetHeimdallAars.Scenario scenario) : IClassFixture<GetHeimdallAars.Scenario>
{
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To   = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        private static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public HeimdallAarsResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetHeimdallAarsAsync(HeimdallPowerLineId, From, To).GetAwaiter().GetResult();
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), HeimdallPowerLineId);
        }

        public LineAssets Line { get; }
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
    public void ResultShouldHaveAarsList()
    {
        // The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
        Assert.NotNull(scenario.Result?.HeimdallAars);
    }

    [Fact]
    public void AllAarsShouldHaveTimestampsWithinRequestedRange()
    {
        Assert.All(scenario.Result!.HeimdallAars, aar =>
        {
            Assert.True(aar.Timestamp >= From, $"Timestamp {aar.Timestamp} is before {From}");
            Assert.True(aar.Timestamp <= To,   $"Timestamp {aar.Timestamp} is after {To}");
        });
    }

    [Fact]
    public void AllAarsShouldHavePositiveValues()
    {
        Assert.All(scenario.Result!.HeimdallAars, aar =>
            Assert.True(aar.Value > 0, $"AAR value {aar.Value} at {aar.Timestamp} should be positive"));
    }

    [Fact]
    public void AllAarsShouldBeLimitedAtASpanOnTheLine()
    {
        Assert.All(scenario.Result!.HeimdallAars, aar => Assert.Contains(aar.AtSpanId, scenario.Line.SpanIds));
    }

    [Fact]
    public void HeimdallSpanAarsShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Result?.HeimdallSpanAars);
    }
}

/// <summary>
/// Queries the last six hours of Heimdall AAR for "Heimdall Power Line" with <c>include=spans</c>
/// and cross-checks the per-span series against the asset hierarchy and the line-level series.
/// </summary>
[Trait("Category", "Integration")]
public class GetHeimdallAarsWithSpans(GetHeimdallAarsWithSpans.Scenario scenario)
    : IClassFixture<GetHeimdallAarsWithSpans.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public DateTimeOffset From { get; }
        public DateTimeOffset To { get; }
        public HeimdallAarsResponse Result { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            // include=spans limits the period to 7 days.
            To = DateTimeOffset.UtcNow;
            From = To.AddHours(-6);
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);
            Result = Client.GetHeimdallAarsAsync(Line.LineId, From, To, new() { Include = HeimdallAarInclude.Spans })
                .GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void HeimdallSpanAarsShouldBePresentWithSpanIdsFromAssets_WhenRequested()
    {
        // The list may be empty: spans without any Heimdall AAR in the period are omitted.
        Assert.NotNull(scenario.Result.HeimdallSpanAars);
        Assert.All(scenario.Result.HeimdallSpanAars!, span => Assert.Contains(span.SpanId, scenario.Line.SpanIds));
    }

    [Fact]
    public void AllSpanAarsShouldBePositiveAndAtLineTimestamps()
    {
        // Span values are returned only at the timestamps where the line has a Heimdall AAR.
        var lineTimestamps = scenario.Result.HeimdallAars.Select(aar => aar.Timestamp).ToHashSet();
        Assert.All(scenario.Result.HeimdallSpanAars!.SelectMany(span => span.HeimdallAars), aar =>
        {
            Assert.True(aar.Value > 0, $"Span AAR {aar.Value} at {aar.Timestamp} should be positive");
            Assert.Equal(TimeSpan.Zero, aar.Timestamp.Offset);
            Assert.Contains(aar.Timestamp, lineTimestamps);
        });
    }

    [Fact]
    public void SpanAarsShouldBeOrderedByTimestamp()
    {
        Assert.All(scenario.Result.HeimdallSpanAars!, span =>
        {
            var timestamps = span.HeimdallAars.Select(aar => aar.Timestamp).ToList();
            Assert.Equal(timestamps.Order(), timestamps);
        });
    }
}

