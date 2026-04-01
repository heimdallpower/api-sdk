namespace HeimdallPower.Api.Client.Extensions;

/// <summary>
/// Options for configuring an outbound HTTP proxy.
/// </summary>
public class ProxyOptions
{
    /// <summary>
    /// The proxy server address (e.g., "http://proxy.example.com:8080").
    /// When null, falls back to environment variables if <see cref="UseEnvironmentVariables"/> is true.
    /// </summary>
    public string? Address { get; init; }

    /// <summary>
    /// Username for proxy authentication. Optional.
    /// </summary>
    public string? Username { get; init; }

    /// <summary>
    /// Password for proxy authentication. Optional.
    /// </summary>
    public string? Password { get; init; }

    /// <summary>
    /// List of hosts that should bypass the proxy (e.g., "localhost", "*.internal.com").
    /// Merged with NO_PROXY environment variable entries when <see cref="UseEnvironmentVariables"/> is true.
    /// </summary>
    public List<string>? BypassList { get; init; }

    /// <summary>
    /// When true, reads HTTPS_PROXY, HTTP_PROXY, and NO_PROXY environment variables
    /// as fallback when <see cref="Address"/> is not explicitly set. Defaults to true.
    /// </summary>
    public bool UseEnvironmentVariables { get; init; } = true;
}
