using HeimdallPower.Api.Client.Common;
using System.Net;
using System.Text.Json;
using System.Text.RegularExpressions;

namespace HeimdallPower.Api.Client.REST;

internal class HeimdallApiHttpClient
{
    private HttpClient HttpClient { get; }
    private readonly AccessTokenHeaderRefresher _tokenRefresher;

    private readonly JsonSerializerOptions _jsonSerializerOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true,
        WriteIndented = true
    };

    private static readonly JsonSerializerOptions ProblemDetailsOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    public HeimdallApiHttpClient(IAccessTokenProvider accessTokenProvider, HttpClient httpClient, Dictionary<string, string>? clientMetadata = null)
    {
        HttpClient = httpClient;
        _tokenRefresher = new AccessTokenHeaderRefresher(accessTokenProvider, httpClient, clientMetadata);
    }

    public async Task<T> GetAsync<T>(string url, CancellationToken cancellationToken = default)
    {
        return await ExecuteWithAuthRetry(async () =>
        {
            var response = await HttpClient.GetAsync(url, cancellationToken);
            var jsonString = await HandleResponse(response, cancellationToken);
            return JsonSerializer.Deserialize<T>(jsonString, _jsonSerializerOptions)
                   ?? throw new HeimdallApiException("Failed to deserialize response.", response.StatusCode, url);
        }, cancellationToken);
    }

    private static async Task<string> HandleResponse(HttpResponseMessage response, CancellationToken cancellationToken)
    {
        var content = await response.Content.ReadAsStringAsync(cancellationToken);
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

            var details = problem ?? new ProblemDetails { Detail = $"Request failed with status code {(int)response.StatusCode} {response.StatusCode}: {TruncateBody(content)}" };
            throw new HeimdallApiException(details, response.StatusCode, requestUrl);
        }

        // Handles 502 Bad Gateway, 504 Gateway Timeout, and any other non-success codes
        throw new HeimdallApiException(
            $"Request failed with status code {(int)response.StatusCode} {response.StatusCode}: {TruncateBody(content)}",
            response.StatusCode,
            requestUrl);
    }

    private static string TruncateBody(string content, int maxLength = 200)
    {
        if (string.IsNullOrWhiteSpace(content)) return "(empty body)";
        // Collapse whitespace runs — useful for HTML error pages
        var collapsed = Regex.Replace(content.Trim(), @"\s+", " ");
        return collapsed.Length <= maxLength ? collapsed : collapsed[..maxLength] + "...";
    }

    private async Task<T> ExecuteWithAuthRetry<T>(Func<Task<T>> operationFunc, CancellationToken cancellationToken)
    {
        try
        {
            await _tokenRefresher.EnsureFreshTokenAsync(cancellationToken);
            return await operationFunc();
        }
        catch (UnauthorizedAccessException)
        {
            await _tokenRefresher.ForceRefreshAsync(cancellationToken);
            return await operationFunc();
        }
    }
}
