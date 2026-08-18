using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries the latest circuit transient rating for the facility on "Heimdall Power Line".</summary>
[Trait("Category", "Integration")]
public class GetLatestCircuitTransientRating(GetLatestCircuitTransientRating.Scenario scenario) : IClassFixture<GetLatestCircuitTransientRating.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" facility – c0ad547d-0d06-4f4c-b5dc-d319430902d2
        private static readonly Guid HeimdallPowerFacilityId = Guid.Parse("c0ad547d-0d06-4f4c-b5dc-d319430902d2");

        public LatestCircuitTransientRatingResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetLatestCircuitTransientRatingAsync(HeimdallPowerFacilityId).GetAwaiter().GetResult();
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
    public void ResultShouldHaveTimestamp()
    {
        Assert.NotEqual(default, scenario.Result?.CircuitTransientRating.Timestamp);
    }

    [Fact]
    public void ResultShouldHaveRatings()
    {
        Assert.NotEmpty(scenario.Result!.CircuitTransientRating.Ratings);
    }

    [Fact]
    public void AllRatingsShouldHaveDurationsOfOneHourOrShorter()
    {
        Assert.All(scenario.Result!.CircuitTransientRating.Ratings, rating =>
        {
            Assert.True(rating.DurationMinutes > 0, $"Duration {rating.DurationMinutes} should be positive");
            Assert.True(rating.DurationMinutes <= 60, $"Duration {rating.DurationMinutes} should not exceed 60 minutes");
        });
    }

    [Fact]
    public void AllRatingsShouldHavePositiveValues()
    {
        Assert.All(scenario.Result!.CircuitTransientRating.Ratings, rating =>
            Assert.True(rating.Value > 0, $"Circuit transient rating value {rating.Value} for {rating.DurationMinutes} minutes should be positive"));
    }

    [Fact]
    public void RatingsShouldBeOrderedByDurationAscending()
    {
        var durations = scenario.Result!.CircuitTransientRating.Ratings.Select(rating => rating.DurationMinutes).ToList();
        Assert.Equal(durations.Order(), durations);
    }
}
