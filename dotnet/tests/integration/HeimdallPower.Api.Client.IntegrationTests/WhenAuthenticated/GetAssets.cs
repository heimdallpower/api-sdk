using HeimdallPower.Api.Client.Assets;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

[Trait("Category", "Integration")]
public class GetAssets(GetAssets.Scenario scenario) : IClassFixture<GetAssets.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public Scenario()
        {
            Result = Client.GetAssetsAsync().GetAwaiter().GetResult();
        }

        public AssetsResponse Result { get; }
    }

    [Fact]
    public void ShouldReturnAssets()
    {
        Assert.NotNull(scenario.Result);
    }

    [Fact]
    public void ResultShouldIncludeGridOwners()
    {
        Assert.NotNull(scenario.Result.GridOwners);
    }

    [Fact]
    public void ResultShouldIncludeLines()
    {
        Assert.NotEmpty(scenario.Result.AllLines());
    }

    [Fact]
    public void ResultShouldIncludeFacilities()
    {
        Assert.NotEmpty(scenario.Result.AllFacilities());
    }
}
