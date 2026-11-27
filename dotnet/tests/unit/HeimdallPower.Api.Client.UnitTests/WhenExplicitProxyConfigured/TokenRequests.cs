using System.Net;
using HeimdallPower.Api.Client.Extensions;
using Microsoft.Extensions.DependencyInjection;

namespace HeimdallPower.Api.Client.UnitTests.WhenExplicitProxyConfigured;

/// <summary>
/// Verifies that <see cref="HeimdallApiClientExtensions.AddHeimdallPowerApiClient"/> routes access token
/// requests through the configured proxy: the token client's primary handler carries the proxy.
/// </summary>
[Trait("Category", "Unit")]
public class TokenRequests
{
    [Fact]
    public void ShouldUseConfiguredProxyForTokenClient()
    {
        var services = new ServiceCollection();
        services.AddHeimdallPowerApiClient(o =>
        {
            o.ClientId = "test-id";
            o.ClientSecret = "test-secret";
            o.Proxy = new ProxyOptions { Address = "http://proxy:8080", UseEnvironmentVariables = false };
        });

        var handler = services.BuildServiceProvider()
            .GetRequiredService<IHttpMessageHandlerFactory>()
            .CreateHandler(HeimdallApiClientExtensions.TokenHttpClientName);
        while (handler is DelegatingHandler delegating)
        {
            handler = delegating.InnerHandler!;
        }

        var primary = Assert.IsType<HttpClientHandler>(handler);
        Assert.True(primary.UseProxy);
        Assert.Equal(new Uri("http://proxy:8080"), Assert.IsType<WebProxy>(primary.Proxy).Address);
    }
}
