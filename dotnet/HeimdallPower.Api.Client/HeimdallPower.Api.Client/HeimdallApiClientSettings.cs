namespace HeimdallPower.Api.Client;

/// <summary>
/// Optional settings for <see cref="HeimdallApiClient"/>. Unset properties fall back to the documented defaults.
/// </summary>
public sealed record HeimdallApiClientSettings
{
    /// <summary>
    /// The <see cref="System.Net.Http.HttpClient"/> used for API requests, e.g. one with a custom
    /// <see cref="System.Net.Http.HttpClient.Timeout"/>. Its <see cref="System.Net.Http.HttpClient.BaseAddress"/> must point
    /// at the Heimdall Power API. When null, a client targeting the production API is created.
    /// </summary>
    public HttpClient? HttpClient { get; init; }

    /// <summary>
    /// Additional headers sent with every request, for example to identify the calling application.
    /// </summary>
    public IReadOnlyDictionary<string, string>? ClientMetadata { get; init; }

    /// <summary>
    /// Message handler used when acquiring access tokens, typically one configured with an outbound proxy.
    /// When null, the default handler is used.
    /// </summary>
    public HttpMessageHandler? TokenProxyHandler { get; init; }
}
