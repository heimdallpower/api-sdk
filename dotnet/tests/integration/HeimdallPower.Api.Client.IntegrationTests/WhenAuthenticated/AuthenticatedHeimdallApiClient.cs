using HeimdallPower.Api.Client.Extensions;
using Microsoft.Extensions.DependencyInjection;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

public class AuthenticatedHeimdallApiClient
{
    protected readonly HeimdallApiClient Client;

    protected AuthenticatedHeimdallApiClient()
    {
        var clientSecret = Environment.GetEnvironmentVariable("HEIMDALL_CLIENT_SECRET") ?? throw new InvalidOperationException("HEIMDALL_CLIENT_SECRET environment variable is not set.");
        var clientId = Environment.GetEnvironmentVariable("HEIMDALL_CLIENT_ID") ?? throw new InvalidOperationException("HEIMDALL_CLIENT_ID environment variable is not set.");
        var clientMetadata = new Dictionary<string, string>
        {
            { "c-client-name", "HeimdallPower.Api.Client.IntegrationTests" },
            { "c-client-version", "0.0.0" },
        };

        var services = new ServiceCollection();

        services.AddHeimdallPowerApiClient(options =>
        {
            options.ClientId = clientId;
            options.ClientSecret = clientSecret;
            options.ClientMetadata = clientMetadata;
        });

        var provider = services.BuildServiceProvider();
        Client = provider.GetRequiredService<HeimdallApiClient>();
    }
}
