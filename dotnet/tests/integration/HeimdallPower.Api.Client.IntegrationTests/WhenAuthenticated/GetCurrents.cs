using HeimdallPower.Api.Client.GridInsights.Lines;

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
}

