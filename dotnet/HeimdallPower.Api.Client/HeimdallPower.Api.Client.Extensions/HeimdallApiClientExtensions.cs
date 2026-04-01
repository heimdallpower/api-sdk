using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

namespace HeimdallPower.Api.Client.Extensions;

/// <summary>
/// Extension methods for adding the Heimdall Power API client to the service collection.
/// </summary>
public static class HeimdallApiClientExtensions
{
    /// <summary>
    /// Adds the Heimdall Power API client to the service collection.
    /// The client is using standard resilience handlers to handle transient errors.
    /// </summary>
    /// <param name="services"></param>
    /// <param name="configureOptions"></param>
    /// <returns></returns>
    public static IServiceCollection AddHeimdallPowerApiClient(this IServiceCollection services, Action<HeimdallApiClientOptions> configureOptions)
    {
        const string clientName = "HeimdallPower";

        services.Configure(configureOptions);

        services.AddHttpClient(clientName)
            .ConfigureHttpClient((_, client) =>
            {
                client.BaseAddress = new Uri("https://external-api.heimdallcloud.com");
                client.DefaultRequestHeaders.Add("Accept", "application/json");
            })
            .ConfigurePrimaryHttpMessageHandler(sp =>
            {
                var options = sp.GetRequiredService<IOptions<HeimdallApiClientOptions>>().Value;
                return ProxyHandlerFactory.CreateHandler(options.Proxy) ?? new HttpClientHandler();
            })
            .AddStandardResilienceHandler();

        services.AddSingleton(sp =>
        {
            var options = sp.GetRequiredService<IOptions<HeimdallApiClientOptions>>().Value;
            var httpClientFactory = sp.GetRequiredService<IHttpClientFactory>();
            var httpClient = httpClientFactory.CreateClient(clientName);
            var proxyHandler = ProxyHandlerFactory.CreateHandler(options.Proxy);

            return new HeimdallApiClient(options.ClientId, options.ClientSecret, httpClient, options.ClientMetadata, proxyHandler);
        });

        services.AddSingleton<IHeimdallApiClient>(sp => sp.GetRequiredService<HeimdallApiClient>());

        return services;
    }
}
