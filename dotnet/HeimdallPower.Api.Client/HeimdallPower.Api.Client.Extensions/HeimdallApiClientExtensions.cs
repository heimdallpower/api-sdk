using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Options;

namespace HeimdallPower.Api.Client.Extensions;

/// <summary>
/// Extension methods for adding the Heimdall Power API client to the service collection.
/// </summary>
public static class HeimdallApiClientExtensions
{
    internal const string ApiHttpClientName = "HeimdallPower";
    internal const string TokenHttpClientName = "HeimdallPower.Token";

    /// <summary>
    /// Adds the Heimdall Power API client to the service collection.
    /// The client is using standard resilience handlers to handle transient errors,
    /// for both API calls and access token requests.
    /// </summary>
    /// <param name="services"></param>
    /// <param name="configureOptions"></param>
    /// <returns></returns>
    public static IServiceCollection AddHeimdallPowerApiClient(this IServiceCollection services, Action<HeimdallApiClientOptions> configureOptions)
    {
        services.Configure(configureOptions);

        services.AddHttpClient(ApiHttpClientName)
            .ConfigureHttpClient((_, client) =>
            {
                client.BaseAddress = new Uri("https://external-api.heimdallcloud.com");
                client.DefaultRequestHeaders.Add("Accept", "application/json");
            })
            .ConfigurePrimaryHttpMessageHandler(CreatePrimaryHandler)
            .AddStandardResilienceHandler();

        services.AddHttpClient(TokenHttpClientName)
            .ConfigurePrimaryHttpMessageHandler(CreatePrimaryHandler)
            .AddStandardResilienceHandler();

        services.AddSingleton(sp =>
        {
            var options = sp.GetRequiredService<IOptions<HeimdallApiClientOptions>>().Value;
            var httpClientFactory = sp.GetRequiredService<IHttpClientFactory>();

            return new HeimdallApiClient(options.ClientId, options.ClientSecret, new HeimdallApiClientSettings
            {
                HttpClient = httpClientFactory.CreateClient(ApiHttpClientName),
                ClientMetadata = options.ClientMetadata,
                TokenHttpClient = httpClientFactory.CreateClient(TokenHttpClientName),
            });
        });

        services.AddSingleton<IHeimdallApiClient>(sp => sp.GetRequiredService<HeimdallApiClient>());

        return services;
    }

    private static HttpMessageHandler CreatePrimaryHandler(IServiceProvider sp)
    {
        var options = sp.GetRequiredService<IOptions<HeimdallApiClientOptions>>().Value;
        return ProxyHandlerFactory.CreateHandler(options.Proxy) ?? new HttpClientHandler();
    }
}
