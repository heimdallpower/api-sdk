using System.Net;

namespace HeimdallPower.Api.Client.Extensions;

/// <summary>
/// Creates <see cref="HttpClientHandler"/> instances configured with proxy settings.
/// </summary>
internal static class ProxyHandlerFactory
{
    /// <summary>
    /// Creates an <see cref="HttpClientHandler"/> with proxy settings from the given options,
    /// falling back to HTTPS_PROXY/HTTP_PROXY/NO_PROXY environment variables.
    /// Returns null if no proxy is configured.
    /// </summary>
    internal static HttpClientHandler? CreateHandler(ProxyOptions? options)
    {
        if (options == null)
            return null;

        var proxyAddress = options.Address;

        if (string.IsNullOrEmpty(proxyAddress) && options.UseEnvironmentVariables)
        {
            proxyAddress = Environment.GetEnvironmentVariable("HTTPS_PROXY")
                           ?? Environment.GetEnvironmentVariable("https_proxy")
                           ?? Environment.GetEnvironmentVariable("HTTP_PROXY")
                           ?? Environment.GetEnvironmentVariable("http_proxy");
        }

        if (string.IsNullOrEmpty(proxyAddress))
            return null;

        var proxy = new WebProxy(proxyAddress);

        if (!string.IsNullOrEmpty(options.Username))
        {
            proxy.Credentials = new NetworkCredential(options.Username, options.Password);
        }

        var bypassList = BuildBypassList(options);
        if (bypassList.Length > 0)
        {
            proxy.BypassList = bypassList;
        }

        return new HttpClientHandler
        {
            UseProxy = true,
            Proxy = proxy
        };
    }

    private static string[] BuildBypassList(ProxyOptions options)
    {
        var entries = new List<string>();

        if (options.BypassList != null)
        {
            foreach (var entry in options.BypassList)
            {
                var regex = ConvertToBypassRegex(entry);
                if (!string.IsNullOrEmpty(regex))
                    entries.Add(regex);
            }
        }

        if (options.UseEnvironmentVariables)
        {
            var noProxy = Environment.GetEnvironmentVariable("NO_PROXY")
                          ?? Environment.GetEnvironmentVariable("no_proxy");

            if (!string.IsNullOrEmpty(noProxy))
            {
                foreach (var entry in noProxy.Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries))
                {
                    var regex = ConvertToBypassRegex(entry);
                    if (!string.IsNullOrEmpty(regex))
                        entries.Add(regex);
                }
            }
        }

        return entries.ToArray();
    }

    /// <summary>
    /// Converts a NO_PROXY-style entry (e.g., "*.example.com", ".example.com", "localhost")
    /// to a regex pattern compatible with <see cref="WebProxy.BypassList"/>.
    /// </summary>
    private static string ConvertToBypassRegex(string entry)
    {
        if (string.IsNullOrWhiteSpace(entry))
            return string.Empty;

        // Leading dot means match the domain and all subdomains (e.g., ".example.com" -> "*.example.com")
        if (entry.StartsWith('.'))
            entry = "*" + entry;

        // Escape dots and convert wildcard * to regex .*
        var regex = entry
            .Replace(".", "\\.")
            .Replace("*", ".*");

        return regex;
    }
}
