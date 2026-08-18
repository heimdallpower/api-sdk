using HeimdallPower.Api.Client.CapacityMonitoring.Lines;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

/// <summary>Queries the latest line transient rating for "Heimdall Power Line".</summary>
[Trait("Category", "Integration")]
public class GetLatestLineTransientRating(GetLatestLineTransientRating.Scenario scenario) : IClassFixture<GetLatestLineTransientRating.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        // "Heimdall Power Line" – d67d2205-6629-4bbd-aa9f-436bf22842ad
        private static readonly Guid HeimdallPowerLineId = Guid.Parse("d67d2205-6629-4bbd-aa9f-436bf22842ad");

        public LatestLineTransientRatingResponse? Result { get; }

        public Scenario()
        {
            Result = Client.GetLatestLineTransientRatingAsync(HeimdallPowerLineId).GetAwaiter().GetResult();
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
        Assert.NotEqual(default, scenario.Result?.LineTransientRating.Timestamp);
    }

    [Fact]
    public void ResultShouldHaveRatings()
    {
        Assert.NotEmpty(scenario.Result!.LineTransientRating.Ratings);
    }

    [Fact]
    public void AllRatingsShouldHaveDurationsOfOneHourOrShorter()
    {
        Assert.All(scenario.Result!.LineTransientRating.Ratings, rating =>
        {
            Assert.True(rating.DurationMinutes > 0, $"Duration {rating.DurationMinutes} should be positive");
            Assert.True(rating.DurationMinutes <= 60, $"Duration {rating.DurationMinutes} should not exceed 60 minutes");
        });
    }

    [Fact]
    public void AllRatingsShouldHavePositiveValues()
    {
        Assert.All(scenario.Result!.LineTransientRating.Ratings, rating =>
            Assert.True(rating.Value > 0, $"Transient rating value {rating.Value} for {rating.DurationMinutes} minutes should be positive"));
    }

    [Fact]
    public void RatingsShouldBeOrderedByDurationAscending()
    {
        var durations = scenario.Result!.LineTransientRating.Ratings.Select(rating => rating.DurationMinutes).ToList();
        Assert.Equal(durations.Order(), durations);
    }
}
