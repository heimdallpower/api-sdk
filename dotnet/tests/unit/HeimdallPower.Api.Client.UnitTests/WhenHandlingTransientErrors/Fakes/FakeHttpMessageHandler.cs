using System.Net;
using System.Net.Http.Headers;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingTransientErrors.Fakes;

/// <summary>
/// Returns a pre-configured sequence of HttpResponseMessages.
/// When the sequence is exhausted it keeps returning the last entry.
/// </summary>
internal sealed class FakeHttpMessageHandler : HttpMessageHandler
{
    private readonly Queue<HttpResponseMessage> _responses;
    private HttpResponseMessage _lastResponse;

    public int CallCount { get; private set; }

    public FakeHttpMessageHandler(params HttpResponseMessage[] responses)
    {
        if (responses.Length == 0)
            throw new ArgumentException("Provide at least one response.", nameof(responses));

        _responses = new Queue<HttpResponseMessage>(responses);
        _lastResponse = responses[^1];
    }

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        CallCount++;
        if (_responses.TryDequeue(out var response))
            _lastResponse = response;

        return Task.FromResult(_lastResponse);
    }

    // ------------------------------------------------------------------
    // Factory helpers
    // ------------------------------------------------------------------

    /// <summary>Returns an HTML response that Application Gateway sends on 504/500.</summary>
    public static HttpResponseMessage HtmlResponse(HttpStatusCode statusCode, string? htmlBody = null)
    {
        htmlBody ??= """
                     <!DOCTYPE html>
                     <html><head><title>Gateway Timeout</title></head>
                     <body><h1>504 Gateway Timeout</h1>
                     <p>The server did not respond in time.</p>
                     </body></html>
                     """;

        var response = new HttpResponseMessage(statusCode)
        {
            Content = new StringContent(htmlBody)
        };
        response.Content.Headers.ContentType = new MediaTypeHeaderValue("text/html");
        return response;
    }

    /// <summary>Returns a valid 200 JSON response.</summary>
    public static HttpResponseMessage JsonOkResponse(string json)
    {
        var response = new HttpResponseMessage(HttpStatusCode.OK)
        {
            Content = new StringContent(json)
        };
        response.Content.Headers.ContentType = new MediaTypeHeaderValue("application/json");
        return response;
    }

    /// <summary>Returns a 200 response with a minimal ApiResponse wrapper.</summary>
    public static HttpResponseMessage OkApiResponse(string dataJson)
        => JsonOkResponse($$"""{"data":{{dataJson}},"status":"success"}""");
}

