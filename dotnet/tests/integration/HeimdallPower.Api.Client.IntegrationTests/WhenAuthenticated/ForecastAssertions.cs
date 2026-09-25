using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Assertions shared by the forecast scenarios that compare amperes with MVA.</summary>
internal static class ForecastAssertions
{
    public static void AssertApparentPowerOf(IReadOnlyCollection<ForecastDto> mva, IReadOnlyCollection<ForecastDto> amperes, LineAssets line)
    {
        Assert.Equal(amperes.Select(f => f.Timestamp), mva.Select(f => f.Timestamp));
        Assert.All(amperes.Zip(mva), pair =>
        {
            var (a, s) = pair;
            foreach (var (name, amp, apparent) in new[]
                     {
                         ("prediction", a.Prediction, s.Prediction), ("p80", a.P80, s.P80), ("p90", a.P90, s.P90),
                         ("p95", a.P95, s.P95), ("p99", a.P99, s.P99),
                     })
            {
                Assert.True(apparent.Value > 0, $"Forecast {name} at {a.Timestamp}: apparent power {apparent.Value} should be positive");
                line.AssertIsApparentPowerOf(apparent.Value, amp.Value, $"Forecast {name} at {a.Timestamp}");
                Assert.Equal(amp.AtSpanId, apparent.AtSpanId);
            }
        });
    }

    public static void AssertAtSpanIdsOnLine(IReadOnlyCollection<ForecastDto> forecasts, LineAssets line)
    {
        var atSpanIds = forecasts
            .SelectMany(f => new[] { f.Prediction, f.P80, f.P90, f.P95, f.P99 })
            .Select(p => p.AtSpanId)
            .OfType<Guid>();
        Assert.All(atSpanIds, spanId => Assert.Contains(spanId, line.SpanIds));
    }

    public static void AssertApparentPowerOf(IReadOnlyList<CircuitRatingForecastDto> mva, IReadOnlyList<CircuitRatingForecastDto> amperes, LineAssets line)
    {
        Assert.Equal(amperes.Select(f => f.Timestamp), mva.Select(f => f.Timestamp));
        Assert.All(amperes.Zip(mva), pair =>
        {
            var (a, s) = pair;
            foreach (var (name, amp, apparent) in new[]
                     {
                         ("prediction", a.Prediction, s.Prediction), ("p80", a.P80, s.P80), ("p90", a.P90, s.P90),
                         ("p95", a.P95, s.P95), ("p99", a.P99, s.P99),
                     })
            {
                Assert.True(apparent.Value > 0, $"Forecast {name} at {a.Timestamp}: apparent power {apparent.Value} should be positive");
                line.AssertIsApparentPowerOf(apparent.Value, amp.Value, $"Forecast {name} at {a.Timestamp}");
                Assert.Equal(amp.AtFacilityComponentId, apparent.AtFacilityComponentId);
            }
        });
    }
}
