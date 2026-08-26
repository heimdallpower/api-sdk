namespace HeimdallPower.Api.Client.Extensions;

/// <summary>
/// Options for configuring the Heimdall Power stream client.
/// </summary>
public class HeimdallStreamClientOptions
{
    /// <summary>
    /// The client ID for the Heimdall Power API.
    /// </summary>
    public required string ClientId { get; set; }

    /// <summary>
    /// The client secret for the Heimdall Power API.
    /// </summary>
    public required string ClientSecret { get; set; }

    /// <summary>
    /// Additional metadata to include in the request headers.
    /// </summary>
    public Dictionary<string, string>? ClientMetadata { get; set; }

    /// <summary>
    /// Optional proxy configuration. When set, all HTTP requests (stream connection and token acquisition)
    /// are routed through the specified proxy.
    /// </summary>
    public ProxyOptions? Proxy { get; set; }
}
