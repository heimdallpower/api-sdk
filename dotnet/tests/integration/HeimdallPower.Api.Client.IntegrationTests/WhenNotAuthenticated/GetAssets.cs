namespace HeimdallPower.Api.Client.IntegrationTests.WhenNotAuthenticated;

[Trait("Category", "Integration")]
public class GetAssets(GetAssets.Scenario scenario) : IClassFixture<GetAssets.Scenario>
{
    public class Scenario
    {
        public Scenario()
        {
            const string clientSecret = "invalid-client-secret";
            const string clientId = "invalid-client-id";
            Client = new HeimdallApiClient(clientId, clientSecret,new Dictionary<string, string>
            {
                { "c-client-name", "HeimdallPower.Api.Client.IntegrationTests" },
                { "c-client-version", "0.0.0" },
            });
        }

        public HeimdallApiClient Client { get; }
    }

    [Fact]
    public async Task ShouldThrowUnauthorizedException()
    {
        var exception = await Assert.ThrowsAsync<UnauthorizedAccessException>(() => scenario.Client.GetAssetsAsync());
        Assert.Equal("Failed to acquire access token. Please check your client credentials.", exception.Message);
    }

    [Fact]
    public async Task ShouldThrowMsalInnerException()
    {
        var exception = await Assert.ThrowsAsync<UnauthorizedAccessException>(() => scenario.Client.GetAssetsAsync());
        Assert.IsType<Microsoft.Identity.Client.MsalServiceException>(exception.InnerException);
    }
}
