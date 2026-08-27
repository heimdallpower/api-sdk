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
    /// Registers <see cref="IHeimdallStreamClient"/> as a singleton, configured via <paramref name="configureOptions"/>.
    /// </summary>
    /// <remarks>
    /// The stream connection reconnects with exponential backoff internally, handled by <see cref="HeimdallStreamClient"/>.
    /// </remarks>
    /// <param name="services">The service collection to add the client to.</param>
    /// <param name="configureOptions">Callback used to set the <see cref="HeimdallStreamClientOptions"/>, such as client credentials and optional proxy settings.</param>
    /// <returns>The same service collection, for chaining.</returns>
    public static IServiceCollection AddHeimdallPowerStreamClient(this IServiceCollection services, Action<HeimdallStreamClientOptions> configureOptions)
    {
        const string clientName = "HeimdallPowerStream";

        services.Configure(configureOptions);

        services.AddHttpClient(clientName)
            .ConfigureHttpClient((_, client) =>
            {
                client.BaseAddress = new Uri("https://stream-api.heimdallcloud.com");
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
