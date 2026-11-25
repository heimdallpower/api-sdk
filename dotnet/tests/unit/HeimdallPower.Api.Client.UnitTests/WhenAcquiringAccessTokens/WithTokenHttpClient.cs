using System.Net;
using HeimdallPower.Api.Client.UnitTests.Fakes;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenAcquiringAccessTokens;

/// <summary>
/// Verifies <see cref="HeimdallApiClientSettings.TokenHttpClient"/>: token requests go through the given
/// client, the token library adds no retry of its own on top of it, and it cannot be combined with
/// <see cref="HeimdallApiClientSettings.TokenProxyHandler"/>.
/// </summary>
[Trait("Category", "Unit")]
public class WithTokenHttpClient
{
    private const string EmptyAssetsJson = """{"data":{"grid_owners":[]}}""";

    private readonly RecordingHttpMessageHandler _api = new(EmptyAssetsJson);

    private HeimdallApiClient CreateClient(CountingHttpMessageHandler tokenHandler) =>
        new("test-id", "test-secret", new HeimdallApiClientSettings
        {
            HttpClient = new HttpClient(_api) { BaseAddress = new Uri("https://fake-api.example.com") },
            TokenHttpClient = new HttpClient(tokenHandler),
        });

    [Fact]
    public async Task ShouldSendTokenRequestsThroughTokenHttpClient()
    {
        HttpRequestMessage? tokenRequest = null;
        var token = new CountingHttpMessageHandler(request =>
        {
            tokenRequest = request;
            return TokenEndpoint.Token();
        });

        await CreateClient(token).GetAssetsAsync();

        Assert.Equal(1, token.CallCount);
        Assert.Equal(HttpMethod.Post, tokenRequest!.Method);
        Assert.Equal("hpadb2cprod.b2clogin.com", tokenRequest.RequestUri!.Host);
        Assert.EndsWith("/oauth2/v2.0/token", tokenRequest.RequestUri.AbsolutePath);
        Assert.Equal("/assets/v1/assets", _api.LastRequest.RequestUri!.AbsolutePath);
        Assert.Equal($"Bearer {TokenEndpoint.AccessToken}", _api.LastRequest.Headers.Authorization?.ToString());
    }

    [Fact]
    public async Task ShouldNotAddTokenLibraryRetry_WhenTokenEndpointReturns5xx()
    {
        var token = new CountingHttpMessageHandler(_ => TokenEndpoint.Error(HttpStatusCode.ServiceUnavailable, "temporarily_unavailable"));

        await Assert.ThrowsAsync<UnauthorizedAccessException>(() => CreateClient(token).GetAssetsAsync());

        // Retrying is left to the TokenHttpClient; with the token library's own retry on 5xx this would be 2.
        Assert.Equal(1, token.CallCount);
        Assert.Empty(_api.Requests);
    }

    [Fact]
    public void ShouldThrow_WhenTokenProxyHandlerIsAlsoSet()
    {
        var settings = new HeimdallApiClientSettings
        {
            TokenHttpClient = new HttpClient(),
            TokenProxyHandler = new HttpClientHandler(),
        };

        var exception = Assert.Throws<ArgumentException>(() => new HeimdallApiClient("test-id", "test-secret", settings));

        Assert.Equal("settings", exception.ParamName);
    }
}
