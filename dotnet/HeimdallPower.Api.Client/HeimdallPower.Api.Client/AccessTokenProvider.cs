using System.IdentityModel.Tokens.Jwt;
using Microsoft.Identity.Client;

namespace HeimdallPower.Api.Client;

internal interface IAccessTokenProvider
{
    Task AcquireTokenAsync();
    DateTimeOffset GetTokenExpiry();
    IDictionary<string, string> GetAccessHeaders();
}

internal class AccessTokenProvider(string clientId, string clientSecret, string authority, string scope) : IAccessTokenProvider
{
    private readonly IConfidentialClientApplication _msalClient = ConfidentialClientApplicationBuilder.Create(clientId)
        .WithClientSecret(clientSecret)
        .WithAuthority(authority)
        .Build();

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
            { "Region", GetRegion() }
        };
    }
}
