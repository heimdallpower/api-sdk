using System.Net;
using System.Reflection;

namespace HeimdallPower.Api.Client;

public class AuthenticationHandler : DelegatingHandler
{
    private readonly IAccessTokenProvider _tokenProvider;
    private readonly Dictionary<string, string>? _clientMetadata;
    private readonly SemaphoreSlim _tokenLock = new(1, 1);
    private DateTimeOffset _tokenExpiresOn;
    private static readonly TimeSpan TokenExpirationBuffer = TimeSpan.FromMinutes(2);

    internal AuthenticationHandler(
        IAccessTokenProvider tokenProvider,
        Dictionary<string, string>? clientMetadata = null)
    {
        _tokenProvider = tokenProvider;
        _clientMetadata = clientMetadata;
    }

    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        await EnsureValidTokenAsync();
        AddHeaders(request);

        var response = await base.SendAsync(request, cancellationToken);

        if (response.StatusCode == HttpStatusCode.Unauthorized)
        {
            await RefreshTokenAsync();
            AddHeaders(request);
            response = await base.SendAsync(request, cancellationToken);
        }

        return response;
    }

    private async Task EnsureValidTokenAsync()
    {
        if (_tokenExpiresOn == default || DateTimeOffset.UtcNow.Add(TokenExpirationBuffer) > _tokenExpiresOn)
        {
            await RefreshTokenAsync();
        }
    }

    private async Task RefreshTokenAsync()
    {
        await _tokenLock.WaitAsync(TimeSpan.FromSeconds(30));
        try
        {
            // Prevent double refresh if another thread just refreshed
            if (DateTimeOffset.UtcNow.Add(TokenExpirationBuffer) <= _tokenExpiresOn)
                return;

            await _tokenProvider.AcquireTokenAsync();
            _tokenExpiresOn = _tokenProvider.GetTokenExpiry();
        }
        finally
        {
            _tokenLock.Release();
        }
    }

    private static readonly string AssemblyVersion = Assembly.GetExecutingAssembly().GetName().Version?.ToString() ?? "0.0.0";
    private const string ClientName = "dotnet-sdk";

    /// <summary>
    /// Builds the client headers to be sent with each request.
    /// Includes client name, version, and any additional metadata provided.
    /// </summary>
    /// <returns></returns>
    private Dictionary<string, string> BuildClientHeaders()
    {
        var headers = new Dictionary<string, string>
        {
            { "x-client-name", ClientName },
            { "x-client-version", AssemblyVersion },
        };

        if (_clientMetadata != null)
        {
            foreach (var kvp in _clientMetadata)
            {
                headers[kvp.Key] = kvp.Value; // Overwrite defaults if present
            }
        }

        return headers;
    }

    private void AddHeaders(HttpRequestMessage request)
    {
        foreach (var header in _tokenProvider.GetAccessHeaders())
        {
            request.Headers.TryAddWithoutValidation(header.Key, header.Value);
        }
        foreach (var header in BuildClientHeaders())
        {
            if (header.Key.Equals("x-region", StringComparison.OrdinalIgnoreCase))
            {
                continue; // Skip adding x-region as this should be set from the token
            }

            request.Headers.TryAddWithoutValidation(header.Key, header.Value);
        }
    }
}
