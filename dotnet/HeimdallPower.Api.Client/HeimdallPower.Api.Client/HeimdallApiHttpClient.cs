using System.Net;
using System.Reflection;
using System.Text.Json;

namespace HeimdallPower.Api.Client;

internal class HeimdallApiHttpClient(IAccessTokenProvider accessTokenProvider, HttpClient httpClient, Dictionary<string, string>? clientMetadata = null)
{
    private HttpClient HttpClient { get; } = httpClient;

    private readonly SemaphoreSlim _tokenLock = new(1, 1);

    private readonly JsonSerializerOptions _jsonSerializerOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true,
        WriteIndented = true
    };

    private DateTimeOffset _tokenExpiresOn;
    private static readonly TimeSpan TokenExpirationBuffer = TimeSpan.FromMinutes(2);

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

        if (clientMetadata != null)
        {
            foreach (var kvp in clientMetadata)
            {
                headers[kvp.Key] = kvp.Value; // Overwrite defaults if present
            }
        }

        return headers;
    }

    private async Task RefreshAccessToken()
    {
        await _tokenLock.WaitAsync(TimeSpan.FromSeconds(30));
        try
        {
            // Check if another thread already refreshed while we were waiting
            if (_tokenExpiresOn != default && DateTimeOffset.UtcNow.Add(TokenExpirationBuffer) <= _tokenExpiresOn)
                return;

            await accessTokenProvider.AcquireTokenAsync();
            _tokenExpiresOn = accessTokenProvider.GetTokenExpiry();

            foreach (var header in accessTokenProvider.GetAccessHeaders())
            {
                HttpClient.DefaultRequestHeaders.Remove(header.Key);
                HttpClient.DefaultRequestHeaders.TryAddWithoutValidation(header.Key, header.Value);
            }
            foreach (var header in BuildClientHeaders())
            {
                if (header.Key.Equals("x-region", StringComparison.OrdinalIgnoreCase))
                {
                    continue; // Skip adding x-region as this should be set from the token
                }

                HttpClient.DefaultRequestHeaders.Remove(header.Key);
                HttpClient.DefaultRequestHeaders.TryAddWithoutValidation(header.Key, header.Value);
            }
        }
        finally
        {
            _tokenLock.Release();
        }
    }
}
