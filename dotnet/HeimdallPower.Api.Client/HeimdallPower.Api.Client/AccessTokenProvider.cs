using System.IdentityModel.Tokens.Jwt;
using Microsoft.Identity.Client;

namespace HeimdallPower.Api.Client;

internal interface IAccessTokenProvider
{
    Task AcquireTokenAsync();
    DateTimeOffset GetTokenExpiry();
    IDictionary<string, string> GetAccessHeaders();
}

internal class AccessTokenProvider(
    string clientId,
    string clientSecret,
    string authority,
    string scope,
    HttpMessageHandler? proxyHandler = null) : IAccessTokenProvider
{
    private readonly IConfidentialClientApplication _msalClient = BuildMsalClient(clientId, clientSecret, authority, proxyHandler);

    private static IConfidentialClientApplication BuildMsalClient(
        string clientId, string clientSecret, string authority, HttpMessageHandler? proxyHandler)
    {
        var builder = ConfidentialClientApplicationBuilder.Create(clientId)
            .WithClientSecret(clientSecret)
            .WithAuthority(authority);

        if (proxyHandler != null)
        {
            builder.WithHttpClientFactory(new MsalProxyHttpClientFactory(proxyHandler));
        }

        return builder.Build();
    }

    private AuthenticationResult? _authResult;

    public async Task AcquireTokenAsync()
    {
        try
        {
            _authResult = await _msalClient
                .AcquireTokenForClient([scope])
                .ExecuteAsync();
        }
        catch (MsalException ex)
        {
            throw new UnauthorizedAccessException("Failed to acquire access token. Please check your client credentials.", ex);
        }
    }

    public DateTimeOffset GetTokenExpiry()
    {
        if (_authResult == null) throw new InvalidOperationException("No access token available.");
        return _authResult?.ExpiresOn ?? DateTimeOffset.MinValue;
    }

    private string GetRegion()
    {
        if (_authResult == null) throw new InvalidOperationException("No access token available.");
        var handler = new JwtSecurityTokenHandler();
        var token = handler.ReadJwtToken(_authResult.AccessToken);
        return token.Claims.First(claim => claim.Type == "region").Value;
    }

    /// <summary>
    /// Gets the access headers required for API request.
    /// Includes the Authorization and Region headers.
    /// </summary>
    /// <returns></returns>
    /// <exception cref="InvalidOperationException"></exception>
    public IDictionary<string, string> GetAccessHeaders()
    {
        if (_authResult == null) throw new InvalidOperationException("No access token available.");
        return new Dictionary<string, string>()
        {
            { "Authorization", $"Bearer {_authResult.AccessToken}" },
            { "x-region", GetRegion() }
        };
    }
}

/// <summary>
/// Adapts an <see cref="HttpMessageHandler"/> to MSAL's <see cref="IMsalHttpClientFactory"/>
/// so that MSAL token requests are routed through a proxy.
/// </summary>
internal class MsalProxyHttpClientFactory(HttpMessageHandler handler) : IMsalHttpClientFactory
{
    public HttpClient GetHttpClient() => new(handler, disposeHandler: false);
}
