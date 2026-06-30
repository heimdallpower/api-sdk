using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries historical circuit ratings for the facility on "Heimdall Power Line" (2026-01-01).</summary>
[Trait("Category", "Integration")]
public class GetCircuitRatings(GetCircuitRatings.Scenario scenario) : IClassFixture<GetCircuitRatings.Scenario>
{
    private static readonly DateTimeOffset From = new(2026, 1, 1, 0, 0, 0, TimeSpan.Zero);
    private static readonly DateTimeOffset To   = new(2026, 1, 2, 0, 0, 0, TimeSpan.Zero);

    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" facility – c0ad547d-0d06-4f4c-b5dc-d319430902d2
        private static readonly Guid HeimdallPowerFacilityId = Guid.Parse("c0ad547d-0d06-4f4c-b5dc-d319430902d2");

        public CircuitRatingsResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetCircuitRatingsAsync(HeimdallPowerFacilityId, From, To).GetAwaiter().GetResult();
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
    public void ResultShouldHaveCircuitRatingsList()
    {
        // The API returns HTTP 200 with a (possibly empty) list – an empty list is valid.
        Assert.NotNull(scenario.Result?.CircuitRatings);
    }

    [Fact]
    public void AllCircuitRatingsShouldHaveTimestampsWithinRequestedRange()
    {
        Assert.All(scenario.Result!.CircuitRatings, cr =>
        {
            Assert.True(cr.Timestamp >= From, $"Timestamp {cr.Timestamp} is before {From}");
            Assert.True(cr.Timestamp <= To,   $"Timestamp {cr.Timestamp} is after {To}");
        });
    }

    [Fact]
    public void AllCircuitRatingsShouldHavePositiveValues()
    {
        Assert.All(scenario.Result!.CircuitRatings, cr =>
            Assert.True(cr.Value > 0, $"Circuit rating value {cr.Value} at {cr.Timestamp} should be positive"));
    }
}

