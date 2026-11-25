using System.Net;
using HeimdallPower.Api.Client.Extensions;
using HeimdallPower.Api.Client.UnitTests.Fakes;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Http.Resilience;
using Microsoft.Extensions.Logging;
using Polly;
using Polly.Timeout;

namespace HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions;

/// <summary>
/// Verifies that <see cref="HeimdallApiClientExtensions.AddHeimdallPowerApiClient"/> sends access token
/// requests through the standard resilience pipeline: transient failures on the token endpoint are
/// retried up to 3 times (4 attempts in all), rejected credentials are not. Uses the real DI registration
/// and token library; only the retry delays are set to zero so the tests run instantly.
/// </summary>
[Trait("Category", "Unit")]
public class WhenTokenRequestFails
{
    private const string EmptyAssetsJson = """{"data":{"grid_owners":[]}}""";

    private readonly RecordingHttpMessageHandler _api = new(EmptyAssetsJson);

    private IHeimdallApiClient Register(CountingHttpMessageHandler tokenHandler, Action<HttpStandardResilienceOptions>? configure = null)
    {
        var services = new ServiceCollection();
        services.AddLogging(b => b.AddDebug());
        services.AddHeimdallPowerApiClient(o =>
        {
            o.ClientId = "test-id";
            o.ClientSecret = "test-secret";
        });
        services.AddHttpClient(HeimdallApiClientExtensions.ApiHttpClientName)
            .ConfigurePrimaryHttpMessageHandler(() => _api);
        services.AddHttpClient(HeimdallApiClientExtensions.TokenHttpClientName)
            .ConfigurePrimaryHttpMessageHandler(() => tokenHandler);

        // AddStandardResilienceHandler names its options "<client name>-standard".
        services.Configure<HttpStandardResilienceOptions>($"{HeimdallApiClientExtensions.TokenHttpClientName}-standard", o =>
        {
            o.Retry.Delay = TimeSpan.Zero;
            o.Retry.BackoffType = DelayBackoffType.Constant;
            o.Retry.UseJitter = false;
            configure?.Invoke(o);
        });

        return services.BuildServiceProvider().GetRequiredService<IHeimdallApiClient>();
    }

    /// <summary>A token endpoint that fails the first <paramref name="failures"/> requests as given, then issues a token.</summary>
    private static CountingHttpMessageHandler FailsThenIssuesToken(int failures, Func<HttpResponseMessage> failure)
    {
        var calls = 0;
        return new CountingHttpMessageHandler(_ => ++calls <= failures ? failure() : TokenEndpoint.Token());
    }

    [Fact]
    public async Task ShouldRetryAndSucceed_WhenTokenConnectionIsResetOnce()
    {
        var token = FailsThenIssuesToken(1, () => throw TokenEndpoint.ConnectionReset());

        var assets = await Register(token).GetAssetsAsync();

        Assert.Empty(assets.GridOwners);
        Assert.Equal(2, token.CallCount);
        Assert.Equal("/assets/v1/assets", _api.LastRequest.RequestUri!.AbsolutePath);
        Assert.Equal($"Bearer {TokenEndpoint.AccessToken}", _api.LastRequest.Headers.Authorization?.ToString());
    }

    // Fails on every retry but the last, so the request only succeeds if all 3 retries are made.
    [Theory]
    [InlineData(HttpStatusCode.ServiceUnavailable)] // 503
    [InlineData(HttpStatusCode.TooManyRequests)]    // 429
    public async Task ShouldRetryAndSucceed_WhenTokenEndpointReturnsTransientStatus(HttpStatusCode statusCode)
    {
        var token = FailsThenIssuesToken(3, () => TokenEndpoint.Error(statusCode, "temporarily_unavailable"));

        await Register(token).GetAssetsAsync();

        Assert.Equal(4, token.CallCount);
        Assert.Equal($"Bearer {TokenEndpoint.AccessToken}", _api.LastRequest.Headers.Authorization?.ToString());
    }

    [Fact]
    public async Task ShouldThrowAfterThreeRetries_WhenTokenConnectionKeepsResetting()
    {
        var token = new CountingHttpMessageHandler(_ => throw TokenEndpoint.ConnectionReset());

        await Assert.ThrowsAsync<HttpRequestException>(() => Register(token).GetAssetsAsync());

        Assert.Equal(4, token.CallCount); // 1 initial + 3 retries
        Assert.Empty(_api.Requests);
    }

    [Fact]
    public async Task ShouldThrowAfterThreeRetries_WhenTokenEndpointKeepsReturning5xx()
    {
        var token = new CountingHttpMessageHandler(_ => TokenEndpoint.Error(HttpStatusCode.ServiceUnavailable, "temporarily_unavailable"));

        await Assert.ThrowsAsync<UnauthorizedAccessException>(() => Register(token).GetAssetsAsync());

        // 1 initial + 3 retries; the client does not acquire a token again after the failed acquisition.
        Assert.Equal(4, token.CallCount);
        Assert.Empty(_api.Requests);
    }

    [Fact]
    public async Task ShouldThrowTimeoutRejectedAfterThreeRetries_WhenTokenEndpointDoesNotAnswer()
    {
        var token = new CountingHttpMessageHandler((_, cancellationToken) => TokenEndpoint.NoResponse(cancellationToken));

        // Short attempt timeout so each attempt times out quickly instead of after the default 10 s.
        await Assert.ThrowsAsync<TimeoutRejectedException>(() =>
            Register(token, o => o.AttemptTimeout.Timeout = TimeSpan.FromMilliseconds(50)).GetAssetsAsync());

        Assert.Equal(4, token.CallCount); // 1 initial + 3 retries, each timed out
        Assert.Empty(_api.Requests);
    }

    [Theory]
    [InlineData(HttpStatusCode.BadRequest)]   // 400
    [InlineData(HttpStatusCode.Unauthorized)] // 401
    public async Task ShouldNotRetry_WhenTokenEndpointRejectsCredentials(HttpStatusCode statusCode)
    {
        var token = new CountingHttpMessageHandler(_ => TokenEndpoint.Error(statusCode, "invalid_client"));

        await Assert.ThrowsAsync<UnauthorizedAccessException>(() => Register(token).GetAssetsAsync());

        Assert.Equal(1, token.CallCount);
        Assert.Empty(_api.Requests);
    }
}
