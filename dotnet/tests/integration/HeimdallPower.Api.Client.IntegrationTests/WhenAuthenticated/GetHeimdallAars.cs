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
}

