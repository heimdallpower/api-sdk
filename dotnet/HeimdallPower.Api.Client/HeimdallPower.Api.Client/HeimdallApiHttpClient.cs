using System.Net;
using System.Reflection;
using System.Text.Json;

namespace HeimdallPower.Api.Client;

internal class HeimdallApiHttpClient(
    IAccessTokenProvider accessTokenProvider,
    HttpClient httpClient,
    Dictionary<string, string>? clientMetadata = null,
    Func<TimeSpan, Task>? delayFunc = null)
{
    /// <summary>Delay implementation — injectable for unit tests to avoid real sleeps.</summary>
    private readonly Func<TimeSpan, Task> _delay = delayFunc ?? Task.Delay;
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

    private static readonly JsonSerializerOptions ProblemDetailsOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    private static readonly HashSet<HttpStatusCode> TransientStatusCodes =
    [
        HttpStatusCode.BadGateway,
        HttpStatusCode.ServiceUnavailable,
        HttpStatusCode.GatewayTimeout,
    ];

    private const int MaxRetryAttempts = 3;

    public async Task<T> GetAsync<T>(string url)
    {
        return await ExecuteWithAuthRetry(async () =>
            await ExecuteWithRetryAsync(async () =>
            {
                var response = await HttpClient.GetAsync(url);
                var jsonString = await HandleResponse(response);
                return JsonSerializer.Deserialize<T>(jsonString, _jsonSerializerOptions)
                       ?? throw new HeimdallApiException("Failed to deserialize response.", response.StatusCode, url);
            }, _delay)
        );
    }

    private static async Task<string> HandleResponse(HttpResponseMessage response)
    {
        var content = await response.Content.ReadAsStringAsync();
        var requestUrl = response.RequestMessage?.RequestUri?.ToString() ?? string.Empty;

        if (response.StatusCode == HttpStatusCode.Unauthorized)
        {
            throw new UnauthorizedAccessException("Unauthorized access. Please check your credentials.");
        }

        if (response.IsSuccessStatusCode)
        {
            return content;
        }

        if (response.StatusCode is HttpStatusCode.BadRequest or HttpStatusCode.InternalServerError or HttpStatusCode.ServiceUnavailable)
        {
            // Application Gateway may return HTML instead of JSON on 5xx errors.
            // Attempt to parse as ProblemDetails, but fall back gracefully if body is not valid JSON.
            ProblemDetails? problem = null;
            try
            {
                problem = JsonSerializer.Deserialize<ProblemDetails>(content, ProblemDetailsOptions);
            }
            catch (JsonException)
            {
                // Body is not valid JSON (e.g. HTML error page from Application Gateway)
            }

            var details = problem ?? new ProblemDetails { Detail = $"Request failed with status code {response.StatusCode}. The server may be temporarily unavailable." };
            throw new HeimdallApiException(details, response.StatusCode, requestUrl);
        }

        // Handles 502 Bad Gateway, 504 Gateway Timeout, and any other non-success codes
        throw new HeimdallApiException(
            $"Request failed with status code {response.StatusCode}. The server may be temporarily unavailable.",
            response.StatusCode,
            requestUrl);
    }

    private static async Task<T> ExecuteWithRetryAsync<T>(Func<Task<T>> operationFunc, Func<TimeSpan, Task> delay)
    {
        var attempt = 0;
        while (true)
        {
            try
            {
                return await operationFunc();
            }
            catch (HeimdallApiException ex) when (TransientStatusCodes.Contains(ex.StatusCode) && attempt < MaxRetryAttempts)
            {
                attempt++;
                await delay(TimeSpan.FromSeconds(Math.Pow(2, attempt - 1))); // 1s, 2s, 4s
            }
            catch (HttpRequestException) when (attempt < MaxRetryAttempts)
            {
                // Network-level failures (connection refused, timeout, DNS, etc.)
                attempt++;
                await delay(TimeSpan.FromSeconds(Math.Pow(2, attempt - 1)));
            }
        }
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
