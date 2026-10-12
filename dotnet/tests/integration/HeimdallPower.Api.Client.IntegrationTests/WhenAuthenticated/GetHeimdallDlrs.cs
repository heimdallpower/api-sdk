using HeimdallPower.Api.Client.CapacityMonitoring.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries historical Heimdall DLR values for "Heimdall Power Line" (2026-01-01).</summary>
[Trait("Category", "Integration")]
public class GetHeimdallDlrs(GetHeimdallDlrs.Scenario scenario) : IClassFixture<GetHeimdallDlrs.Scenario>
{
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To   = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        private static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public HeimdallDlrsResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetHeimdallDlrsAsync(HeimdallPowerLineId, From, To).GetAwaiter().GetResult();
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
    public void ResultShouldHaveDlrsList()
    {
        // The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
        Assert.NotNull(scenario.Result?.HeimdallDlrs);
    }

    [Fact]
    public void AllDlrsShouldHaveTimestampsWithinRequestedRange()
    {
        Assert.All(scenario.Result!.HeimdallDlrs, dlr =>
        {
            Assert.True(dlr.Timestamp >= From, $"Timestamp {dlr.Timestamp} is before {From}");
            Assert.True(dlr.Timestamp <= To,   $"Timestamp {dlr.Timestamp} is after {To}");
        });
    }

    [Fact]
    public void AllDlrsShouldHavePositiveValues()
    {
        Assert.All(scenario.Result!.HeimdallDlrs, dlr =>
            Assert.True(dlr.Value > 0, $"DLR value {dlr.Value} at {dlr.Timestamp} should be positive"));
    }

    [Fact]
    public void AllDlrsShouldBeLimitedAtASpanOnTheLine()
    {
        Assert.All(scenario.Result!.HeimdallDlrs, dlr => Assert.Contains(dlr.AtSpanId, scenario.Line.SpanIds));
    }

    [Fact]
    public void HeimdallSpanDlrsShouldBeNull_WhenNotRequested()
    {
        Assert.Null(scenario.Result?.HeimdallSpanDlrs);
    }
}

/// <summary>
/// Queries the last six hours of Heimdall DLR for "Heimdall Power Line" with <c>include=spans</c>
/// and cross-checks the per-span series against the asset hierarchy and the requested window.
/// </summary>
[Trait("Category", "Integration")]
public class GetHeimdallDlrsWithSpans(GetHeimdallDlrsWithSpans.Scenario scenario)
    : IClassFixture<GetHeimdallDlrsWithSpans.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public DateTimeOffset From { get; }
        public DateTimeOffset To { get; }
        public HeimdallDlrsResponse Result { get; }
        public LineAssets Line { get; }

        public Scenario()
        {
            // include=spans limits the period to 7 days.
            To = DateTimeOffset.UtcNow;
            From = To.AddHours(-6);
            Line = LineAssets.Resolve(Client.GetAssetsAsync().GetAwaiter().GetResult(), LineAssets.HeimdallPowerLineId);
            Result = Client.GetHeimdallDlrsAsync(Line.LineId, From, To, new() { Include = HeimdallDlrInclude.Spans })
                .GetAwaiter().GetResult();
        }
    }

    [Fact]
    public void HeimdallSpanDlrsShouldBePresentWithSpanIdsFromAssets_WhenRequested()
    {
        // The list may be empty: spans without any Heimdall DLR in the period are omitted.
        Assert.NotNull(scenario.Result.HeimdallSpanDlrs);
        Assert.All(scenario.Result.HeimdallSpanDlrs!, span => Assert.Contains(span.SpanId, scenario.Line.SpanIds));
    }

    [Fact]
    public void AllSpanDlrsShouldBePositiveAndWithinRequestedRange()
    {
        Assert.All(scenario.Result.HeimdallSpanDlrs!.SelectMany(span => span.HeimdallDlrs), dlr =>
        {
            Assert.True(dlr.Value > 0, $"Span DLR {dlr.Value} at {dlr.Timestamp} should be positive");
            Assert.Equal(TimeSpan.Zero, dlr.Timestamp.Offset);
            Assert.True(dlr.Timestamp >= scenario.From, $"Timestamp {dlr.Timestamp} is before {scenario.From}");
            Assert.True(dlr.Timestamp <= scenario.To, $"Timestamp {dlr.Timestamp} is after {scenario.To}");
        });
    }

    [Fact]
    public void SpanDlrsShouldBeOrderedByTimestamp()
    {
        Assert.All(scenario.Result.HeimdallSpanDlrs!, span =>
        {
            var timestamps = span.HeimdallDlrs.Select(dlr => dlr.Timestamp).ToList();
            Assert.Equal(timestamps.Order(), timestamps);
        });
    }
}

