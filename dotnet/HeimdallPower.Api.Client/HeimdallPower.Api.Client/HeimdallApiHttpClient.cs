using System.IdentityModel.Tokens.Jwt;
using System.Net;
using System.Net.Http.Headers;
using System.Text.Json;
using Microsoft.Identity.Client;

namespace HeimdallPower.Api.Client;

internal class HeimdallApiHttpClient(string clientId, string clientSecret, HttpClient? httpClient = null)
{
    private HttpClient HttpClient { get; } = httpClient ?? new() { BaseAddress = new Uri(ApiUrl) };

    private readonly SemaphoreSlim _tokenLock = new(1, 1);

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

    private DateTimeOffset _tokenExpiresOn = default;

    public async Task<T> GetAsync<T>(string url)
    {
        return await ExecuteWithAuthRetry(async () =>
        {
            var response = await HttpClient.GetAsync(url);
            var jsonString = await HandleResponse(response);
            return JsonSerializer.Deserialize<T>(jsonString, _jsonSerializerOptions)
                   ?? throw new HeimdallApiException("Failed to deserialize response.", response.StatusCode, url);
        });
    }

    private static async Task<string> HandleResponse(HttpResponseMessage response)
    {
        var content = await response.Content.ReadAsStringAsync();

        if (response.StatusCode == HttpStatusCode.Unauthorized)
        {
            throw new UnauthorizedAccessException("Unauthorized access. Please check your credentials.");
        }

        if (response.IsSuccessStatusCode)
        {
            return content;
        }
        if (response.StatusCode == HttpStatusCode.BadRequest ||
            response.StatusCode == HttpStatusCode.InternalServerError ||
            response.StatusCode == HttpStatusCode.ServiceUnavailable)
        {
            var problem = JsonSerializer.Deserialize<ProblemDetails>(content)
                ?? new ProblemDetails { Detail = "An error occurred while processing the request." };
            throw new HeimdallApiException(problem, response.StatusCode, response.RequestMessage?.RequestUri?.ToString() ?? string.Empty);
        }
        throw new HeimdallApiException($"Request failed with status code {response.StatusCode}: {content}", response.StatusCode, response.RequestMessage?.RequestUri?.ToString() ?? string.Empty);
    }



    private async Task<T> ExecuteWithAuthRetry<T>(Func<Task<T>> operationFunc)
    {
        try
        {
            await UpdateAccessTokenIfExpired();
            return await operationFunc();
        }
        catch (UnauthorizedAccessException)
        {
            await RefreshAccessToken();
            return await operationFunc();
        }
    }

    private async Task UpdateAccessTokenIfExpired()
    {
        if (_tokenExpiresOn == default || DateTimeOffset.UtcNow.Add(TokenExpirationBuffer) > _tokenExpiresOn)
        {
            await RefreshAccessToken();
        }
    }

    private async Task RefreshAccessToken()
    {
        await _tokenLock.WaitAsync();
        try
        {
            var authenticationResult = await _msalClient.AcquireTokenForClient([Scope]).ExecuteAsync();
            var handler = new JwtSecurityTokenHandler();
            var token = handler.ReadJwtToken(authenticationResult.AccessToken);
            var region = token.Claims.First(claim => claim.Type == "region").Value;
            HttpClient.DefaultRequestHeaders.Add("x-region", region);
            _tokenExpiresOn = authenticationResult.ExpiresOn;
            HttpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", authenticationResult.AccessToken);
        }
        finally
        {
            _tokenLock.Release();
        }
    }
}
