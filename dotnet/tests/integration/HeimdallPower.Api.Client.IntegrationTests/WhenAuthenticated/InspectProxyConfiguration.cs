using HeimdallPower.Api.Client.Extensions;
using Microsoft.Extensions.DependencyInjection;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

[Trait("Category", "Integration")]
public class InspectProxyConfiguration
{
    [Fact]
    public void IHeimdallApiClient_ShouldResolveFromDI()
    {
        var services = new ServiceCollection();

        services.AddHeimdallPowerApiClient(options =>
        {
            options.ClientId = "test-client-id";
            options.ClientSecret = "test-client-secret";
        });

        var provider = services.BuildServiceProvider();

        var concrete = provider.GetRequiredService<HeimdallApiClient>();
        var abstraction = provider.GetRequiredService<IHeimdallApiClient>();

        Assert.NotNull(concrete);
        Assert.NotNull(abstraction);
        Assert.Same(concrete, abstraction);
    }

    [Fact]
    public void HeimdallApiClient_ShouldResolve_WithProxyConfigured()
    {
        var services = new ServiceCollection();

        services.AddHeimdallPowerApiClient(options =>
        {
            options.ClientId = "test-client-id";
            options.ClientSecret = "test-client-secret";
            options.Proxy = new ProxyOptions
            {
                Address = "http://test-proxy:8080",
                Username = "proxyuser",
                Password = "proxypass"
            };
        });

        var provider = services.BuildServiceProvider();

        var client = provider.GetRequiredService<HeimdallApiClient>();
        Assert.NotNull(client);
    }

    [Fact]
    public void HeimdallApiClient_ShouldResolve_WithoutProxyConfigured()
    {
        var services = new ServiceCollection();

        services.AddHeimdallPowerApiClient(options =>
        {
            options.ClientId = "test-client-id";
            options.ClientSecret = "test-client-secret";
        });

        var provider = services.BuildServiceProvider();

        var client = provider.GetRequiredService<HeimdallApiClient>();
        Assert.NotNull(client);
    }
}
