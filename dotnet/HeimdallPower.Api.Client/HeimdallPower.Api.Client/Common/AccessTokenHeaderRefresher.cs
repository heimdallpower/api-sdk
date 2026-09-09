namespace HeimdallPower.Api.Client.Common;

/// <summary>
/// Keeps an <see cref="HttpClient"/>'s auth and client headers fresh, coalescing concurrent
/// refresh attempts behind a single in-flight token request.
/// </summary>
internal sealed class AccessTokenHeaderRefresher(
    IAccessTokenProvider accessTokenProvider,
    HttpClient httpClient,
    Dictionary<string, string>? clientMetadata = null)
{
    private static readonly TimeSpan TokenExpirationBuffer = TimeSpan.FromMinutes(2);

    private readonly SemaphoreSlim _tokenLock = new(1, 1);
    private DateTimeOffset _tokenExpiresOn;

    private bool IsTokenFresh => _tokenExpiresOn != default && DateTimeOffset.UtcNow.Add(TokenExpirationBuffer) <= _tokenExpiresOn;

    /// <summary>Refreshes the token only if it is missing or within the expiration buffer.</summary>
    public Task EnsureFreshTokenAsync(CancellationToken cancellationToken) =>
        IsTokenFresh ? Task.CompletedTask : RefreshAsync(force: false, cancellationToken);

    /// <summary>Refreshes the token unconditionally, e.g. after the server rejects it as unauthorized.</summary>
    public Task ForceRefreshAsync(CancellationToken cancellationToken) => RefreshAsync(force: true, cancellationToken);

    private async Task RefreshAsync(bool force, CancellationToken cancellationToken)
    {
        await _tokenLock.WaitAsync(TimeSpan.FromSeconds(30), cancellationToken);
        try
        {
            if (!force && IsTokenFresh)
                return; // Another caller already refreshed while we were waiting.

            await accessTokenProvider.AcquireTokenAsync(cancellationToken);
            _tokenExpiresOn = accessTokenProvider.GetTokenExpiry();

            foreach (var header in accessTokenProvider.GetAccessHeaders())
            {
                httpClient.DefaultRequestHeaders.Remove(header.Key);
                httpClient.DefaultRequestHeaders.TryAddWithoutValidation(header.Key, header.Value);
            }

            foreach (var header in ClientHeaders.Build(clientMetadata))
            {
                if (header.Key.Equals("x-region", StringComparison.OrdinalIgnoreCase))
                    continue; // x-region comes from the token, not client metadata

                httpClient.DefaultRequestHeaders.Remove(header.Key);
                httpClient.DefaultRequestHeaders.TryAddWithoutValidation(header.Key, header.Value);
            }
        }
        finally
        {
            _tokenLock.Release();
        }
    }
}
