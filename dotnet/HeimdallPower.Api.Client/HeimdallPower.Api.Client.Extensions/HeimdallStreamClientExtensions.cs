using HeimdallPower.Api.Client.Stream;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

namespace HeimdallPower.Api.Client.Extensions;

/// <summary>
/// Extension methods for adding the Heimdall Power stream client to the service collection.
/// </summary>
public static class HeimdallStreamClientExtensions
{
    /// <summary>
    /// Adds the Heimdall Power stream client to the service collection.
    /// </summary>
    /// <remarks>
    /// Unlike <see cref="HeimdallApiClientExtensions.AddHeimdallPowerApiClient"/>, no standard resilience
    /// handler is applied: its default total-request timeout would tear down the long-lived streaming
    /// connection. Reconnection is instead handled internally by <see cref="HeimdallStreamClient"/>.
    /// </remarks>
    public static IServiceCollection AddHeimdallPowerStreamClient(this IServiceCollection services, Action<HeimdallStreamClientOptions> configureOptions)
    {
        const string clientName = "HeimdallPowerStream";

        services.Configure(configureOptions);

        services.AddHttpClient(clientName)
            .ConfigureHttpClient((_, client) =>
            {
                client.BaseAddress = new Uri("https://external-api.heimdallcloud.com");
                client.DefaultRequestHeaders.Add("Accept", "text/event-stream");
            })
            .ConfigurePrimaryHttpMessageHandler(sp =>
            {
                var options = sp.GetRequiredService<IOptions<HeimdallStreamClientOptions>>().Value;
                return ProxyHandlerFactory.CreateHandler(options.Proxy) ?? new HttpClientHandler();
            });

        services.AddSingleton(sp =>
        {
            var options = sp.GetRequiredService<IOptions<HeimdallStreamClientOptions>>().Value;
            var httpClientFactory = sp.GetRequiredService<IHttpClientFactory>();
            var httpClient = httpClientFactory.CreateClient(clientName);
            var proxyHandler = ProxyHandlerFactory.CreateHandler(options.Proxy);

            return new HeimdallStreamClient(options.ClientId, options.ClientSecret, httpClient, options.ClientMetadata, proxyHandler);
        });

        services.AddSingleton<IHeimdallStreamClient>(sp => sp.GetRequiredService<HeimdallStreamClient>());

        return services;
    }
}
