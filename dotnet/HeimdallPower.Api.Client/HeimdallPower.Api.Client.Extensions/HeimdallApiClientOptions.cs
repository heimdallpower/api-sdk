namespace HeimdallPower.Api.Client.Extensions;

/// <summary>
/// Options for configuring the Heimdall Power API client.
/// </summary>
public class HeimdallApiClientOptions
{
    /// <summary>
    /// The client ID for the Heimdall Power API.
    /// </summary>
    public required string ClientId { get; init; }

    /// <summary>
    /// The client secret for the Heimdall Power API.
    /// </summary>
    public required string ClientSecret { get; init; }

    /// <summary>
    /// Additional metadata to include in the request headers.
    /// </summary>
    public Dictionary<string, string>? ClientMetadata { get; init; }
}
