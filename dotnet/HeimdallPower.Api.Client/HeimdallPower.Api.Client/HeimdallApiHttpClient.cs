using System.IdentityModel.Tokens.Jwt;
using System.Net.Http.Headers;
using System.Text.Json;
using Microsoft.Identity.Client;

namespace HeimdallPower.Api.Client;

public class HeimdallApiHttpClient(string clientId, string clientSecret)
{
    private HttpClient HttpClient { get; } = new() { BaseAddress = new Uri(ApiUrl) };

    private readonly IConfidentialClientApplication _msalClient = ConfidentialClientApplicationBuilder.Create(clientId)
        .WithClientSecret(clientSecret)
        .WithAuthority(Authority)
        .Build();

    private readonly JsonSerializerOptions _jsonSerializerOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true,
        WriteIndented = true
    };

    private const string ApiUrl = "https://external-api.heimdallcloud.com";
    private const string Policy = "B2C_1A_CLIENTCREDENTIALSFLOW";
    private const string Instance = "https://hpadb2cprod.b2clogin.com";
    private const string Domain = "hpadb2cprod.onmicrosoft.com";
    private const string Scope = $"https://{Domain}/dc5758ae-4eea-416e-9e61-812914d9a49a/.default";
    private const string Authority = $"{Instance}/tfp/{Domain}/{Policy}";

    private DateTimeOffset _tokenExpiresOn;


    public async Task<T?> Get<T>(string url)
    {
        await UpdateAccessTokenIfExpired();
        var response = await HttpClient.GetAsync(url);
        var jsonString = await response.Content.ReadAsStringAsync();

        if (response.IsSuccessStatusCode)
        {
            var result = JsonSerializer.Deserialize<T>(jsonString, _jsonSerializerOptions);
            return result;
        }

        Console.WriteLine($"Request failed with status code: {response.StatusCode}, response: {jsonString}");
        return default;
    }

    private async Task UpdateAccessTokenIfExpired()
    {
        if (DateTimeOffset.UtcNow > _tokenExpiresOn)
        {
            var authenticationResult = await _msalClient.AcquireTokenForClient([Scope]).ExecuteAsync();
            var handler = new JwtSecurityTokenHandler();
            var token = handler.ReadJwtToken(authenticationResult.AccessToken);
            var region = token.Claims.First(claim => claim.Type == "region").Value;
            HttpClient.DefaultRequestHeaders.Add("x-region", region);
            _tokenExpiresOn = authenticationResult.ExpiresOn;
            HttpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", authenticationResult.AccessToken);
        }
    }
}
