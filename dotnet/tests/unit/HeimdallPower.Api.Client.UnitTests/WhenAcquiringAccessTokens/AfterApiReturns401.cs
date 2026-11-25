using System.Net;
using System.Text;
using HeimdallPower.Api.Client.UnitTests.Fakes;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenAcquiringAccessTokens;

/// <summary>
/// Verifies that a 401 from the API (not from the token endpoint) gets the request one more attempt.
/// </summary>
[Trait("Category", "Unit")]
public class AfterApiReturns401
{
    private const string EmptyAssetsJson = """{"data":{"grid_owners":[]}}""";

    private static HttpResponseMessage Assets() =>
        new(HttpStatusCode.OK) { Content = new StringContent(EmptyAssetsJson, Encoding.UTF8, "application/json") };

    [Fact]
    public async Task ShouldRetryRequestOnce_WhenApiReturns401Once()
    {
        var calls = 0;
        var api = new CountingHttpMessageHandler(_ => ++calls == 1 ? new HttpResponseMessage(HttpStatusCode.Unauthorized) : Assets());

        var assets = await HeimdallApiClientFactory.Create(api).GetAssetsAsync();

        Assert.Empty(assets.GridOwners);
        Assert.Equal(2, api.CallCount);
    }

    [Fact]
    public async Task ShouldThrowUnauthorized_WhenApiKeepsReturning401()
    {
        var api = new CountingHttpMessageHandler(_ => new HttpResponseMessage(HttpStatusCode.Unauthorized));

        var exception = await Assert.ThrowsAsync<UnauthorizedAccessException>(() => HeimdallApiClientFactory.Create(api).GetAssetsAsync());

        Assert.Equal("Unauthorized access. Please check your credentials.", exception.Message);
        Assert.Equal(2, api.CallCount);
    }
}
