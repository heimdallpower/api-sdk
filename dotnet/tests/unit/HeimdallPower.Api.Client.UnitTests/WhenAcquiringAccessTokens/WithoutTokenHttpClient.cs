using System.Diagnostics;
using System.Net;
using HeimdallPower.Api.Client.UnitTests.Fakes;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;
using Microsoft.Identity.Client;

namespace HeimdallPower.Api.Client.UnitTests.WhenAcquiringAccessTokens;

/// <summary>
/// Pins the token library's (MSAL) own retry on access token requests, which the README documents for a
/// directly created <see cref="HeimdallApiClient"/> without <see cref="HeimdallApiClientSettings.TokenHttpClient"/>:
/// one retry after 1 s on 5xx or a timeout, none on 429 or connection errors. MSAL arrives transitively through
/// Microsoft.Identity.Web; if an update makes these tests fail, update the README's "Resilience and retry".
/// <see cref="HeimdallApiClientSettings.TokenProxyHandler"/> is the fake transport; MSAL applies the same retry to it.
/// </summary>
[Trait("Category", "Unit")]
public class WithoutTokenHttpClient
{
    private const string EmptyAssetsJson = """{"data":{"grid_owners":[]}}""";

    private readonly RecordingHttpMessageHandler _api = new(EmptyAssetsJson);

    private HeimdallApiClient CreateClient(CountingHttpMessageHandler tokenHandler) =>
        new("test-id", "test-secret", new HeimdallApiClientSettings
        {
            HttpClient = new HttpClient(_api) { BaseAddress = new Uri("https://fake-api.example.com") },
            TokenProxyHandler = tokenHandler,
        });

    [Fact]
    public async Task ShouldRetryOnceAfterOneSecond_WhenTokenEndpointReturns5xx()
    {
        var tokenRequests = new List<HttpRequestMessage>();
        var token = new CountingHttpMessageHandler(request =>
        {
            tokenRequests.Add(request);
            return TokenEndpoint.Error(HttpStatusCode.ServiceUnavailable, "temporarily_unavailable");
        });
        var stopwatch = Stopwatch.StartNew();

        var exception = await Assert.ThrowsAsync<UnauthorizedAccessException>(() => CreateClient(token).GetAssetsAsync());

        Assert.IsType<MsalServiceException>(exception.InnerException);
        Assert.Equal(2, token.CallCount);
        Assert.All(tokenRequests, request =>
        {
            Assert.Equal(HttpMethod.Post, request.Method);
            Assert.Equal("hpadb2cprod.b2clogin.com", request.RequestUri!.Host);
            Assert.EndsWith("/oauth2/v2.0/token", request.RequestUri.AbsolutePath);
        });
        Assert.True(stopwatch.Elapsed >= TimeSpan.FromMilliseconds(900), $"Retried after {stopwatch.Elapsed}, expected about 1 s.");
        Assert.Empty(_api.Requests);
    }

    [Fact]
    public async Task ShouldRetryOnce_WhenTokenRequestTimesOut()
    {
        var token = new CountingHttpMessageHandler(_ => throw TokenEndpoint.TimedOut());

        var exception = await Assert.ThrowsAsync<UnauthorizedAccessException>(() => CreateClient(token).GetAssetsAsync());

        Assert.IsType<MsalServiceException>(exception.InnerException);
        Assert.Equal(2, token.CallCount);
        Assert.Empty(_api.Requests);
    }

    [Fact]
    public async Task ShouldNotRetry_WhenTokenEndpointReturns429()
    {
        var token = new CountingHttpMessageHandler(_ => TokenEndpoint.Error(HttpStatusCode.TooManyRequests, "slow_down"));

        await Assert.ThrowsAsync<UnauthorizedAccessException>(() => CreateClient(token).GetAssetsAsync());

        Assert.Equal(1, token.CallCount);
        Assert.Empty(_api.Requests);
    }

    [Fact]
    public async Task ShouldNotRetry_WhenTokenConnectionIsReset()
    {
        var token = new CountingHttpMessageHandler(_ => throw TokenEndpoint.ConnectionReset());

        await Assert.ThrowsAsync<HttpRequestException>(() => CreateClient(token).GetAssetsAsync());

        Assert.Equal(1, token.CallCount);
        Assert.Empty(_api.Requests);
    }

    [Theory]
    [InlineData(HttpStatusCode.BadRequest)]   // 400
    [InlineData(HttpStatusCode.Unauthorized)] // 401
    public async Task ShouldNotRetry_WhenTokenEndpointRejectsCredentials(HttpStatusCode statusCode)
    {
        var token = new CountingHttpMessageHandler(_ => TokenEndpoint.Error(statusCode, "invalid_client"));

        var exception = await Assert.ThrowsAsync<UnauthorizedAccessException>(() => CreateClient(token).GetAssetsAsync());

        Assert.Equal("Failed to acquire access token. Please check your client credentials.", exception.Message);
        Assert.Equal(1, token.CallCount);
        Assert.Empty(_api.Requests);
    }
}
