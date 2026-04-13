namespace HeimdallPower.Api.Client.UnitTests.WhenBuildingUrls;

[Trait("Category", "Unit")]
public class SagAndClearanceUrl
{
    private static readonly Guid LineId = new("aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee");

    [Fact]
    public void ShouldContainLineId()
    {
        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(LineId);

        Assert.Contains(LineId.ToString(), url);
    }

    [Fact]
    public void ShouldContainSagAndClearanceEndpoint()
    {
        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(LineId);

        Assert.Contains("sag_and_clearance/latest", url);
    }

    [Fact]
    public void ShouldDefaultToMetricUnitSystem()
    {
        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(LineId);

        Assert.Contains("unit_system=metric", url);
    }

    [Fact]
    public void ShouldUseProvidedUnitSystem()
    {
        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(LineId, unitSystem: "imperial");

        Assert.Contains("unit_system=imperial", url);
    }

    [Fact]
    public void ShouldNotIncludeSinceParam_WhenSinceIsNull()
    {
        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(LineId, since: null);

        Assert.DoesNotContain("since=", url);
    }

    [Fact]
    public void ShouldIncludeSinceParam_WhenSinceIsProvided()
    {
        var since = new DateTimeOffset(2024, 1, 15, 12, 34, 56, TimeSpan.Zero);

        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(LineId, since: since);

        Assert.Contains("since=", url);
    }

    [Fact]
    public void ShouldFormatSinceAsUtc()
    {
        var since = new DateTimeOffset(2024, 1, 15, 12, 34, 56, TimeSpan.FromHours(2));

        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(LineId, since: since);

        Assert.Contains("2024-01-15T10%3a34%3a56", url);
    }
}
