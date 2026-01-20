using System.Net;
using System.Reflection;
using System.Text.Json;

namespace HeimdallPower.Api.Client;

internal class HeimdallApiHttpClient(HttpClient httpClient)
{
    private HttpClient HttpClient { get; } = httpClient;

    private readonly JsonSerializerOptions _jsonSerializerOptions = new()
    {
        PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower,
        PropertyNameCaseInsensitive = true,
        WriteIndented = true
    };

    public async Task<T> GetAsync<T>(string url)
    {
        var response = await HttpClient.GetAsync(url);
        var jsonString = await HandleResponse(response);
        return JsonSerializer.Deserialize<T>(jsonString, _jsonSerializerOptions)
               ?? throw new HeimdallApiException("Failed to deserialize response.", response.StatusCode, url);
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
}
