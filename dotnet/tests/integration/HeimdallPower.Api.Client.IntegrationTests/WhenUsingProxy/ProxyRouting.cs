using DotNet.Testcontainers.Builders;
using DotNet.Testcontainers.Containers;
using HeimdallPower.Api.Client.Extensions;
using Microsoft.Extensions.DependencyInjection;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenUsingProxy;

[Trait("Category", "ProxyIntegration")]
public class ProxyRouting : IAsyncLifetime, IDisposable
{
    private readonly IContainer _proxy = new ContainerBuilder()
        .WithImage("ubuntu/squid:latest")
        .WithPortBinding(3128, true)
        .WithResourceMapping(
            "http_port 3128\nacl all src all\nhttp_access allow all\ncache deny all\n"u8.ToArray(),
            "/etc/squid/squid.conf")
        .WithWaitStrategy(Wait.ForUnixContainer().UntilPortIsAvailable(3128))
        .Build();

    private readonly List<string> _envVarsToClean = [];

    public Task InitializeAsync() => _proxy.StartAsync();
    public Task DisposeAsync() => _proxy.DisposeAsync().AsTask();

    public void Dispose()
    {
        foreach (var key in _envVarsToClean)
            Environment.SetEnvironmentVariable(key, null);
    }

    private string ProxyAddress => $"http://localhost:{_proxy.GetMappedPublicPort(3128)}";

    private static (string clientId, string clientSecret) GetCredentials()
    {
        var clientId = Environment.GetEnvironmentVariable("HEIMDALL_CLIENT_ID")
            ?? throw new InvalidOperationException("HEIMDALL_CLIENT_ID environment variable is not set.");
        var clientSecret = Environment.GetEnvironmentVariable("HEIMDALL_CLIENT_SECRET")
            ?? throw new InvalidOperationException("HEIMDALL_CLIENT_SECRET environment variable is not set.");
        return (clientId, clientSecret);
    }

    private IHeimdallApiClient BuildClient(ProxyOptions proxy)
    {
        var (clientId, clientSecret) = GetCredentials();
        var services = new ServiceCollection();
        services.AddHeimdallPowerApiClient(options =>
        {
            options.ClientId = clientId;
            options.ClientSecret = clientSecret;
            options.Proxy = proxy;
        });
        return services.BuildServiceProvider().GetRequiredService<IHeimdallApiClient>();
    }

    [Fact]
    public async Task RequestsAreRoutedThroughProxy()
    {
        var client = BuildClient(new ProxyOptions { Address = ProxyAddress });
        var assets = await client.GetAssetsAsync();
        Assert.NotNull(assets);
    }

    [Fact]
    public async Task EnvVarProxy_RoutesTraffic()
    {
        _envVarsToClean.Add("HTTPS_PROXY");
        Environment.SetEnvironmentVariable("HTTPS_PROXY", ProxyAddress);

        var client = BuildClient(new ProxyOptions { UseEnvironmentVariables = true });
        var assets = await client.GetAssetsAsync();
        Assert.NotNull(assets);
    }
}
