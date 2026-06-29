using System.Net;
using System.Text;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

/// <summary>
/// A minimal <see cref="HttpMessageHandler"/> that invokes a caller-supplied
/// delegate for every request so tests can control the exact HTTP response.
/// </summary>
internal sealed class FakeHttpMessageHandler(Func<HttpRequestMessage, HttpResponseMessage> respond) : HttpMessageHandler
{
    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken) =>
        Task.FromResult(respond(request));

    // ── Convenience factories ────────────────────────────────────────────────

    public static FakeHttpMessageHandler Returns(HttpStatusCode code, string body, string mediaType = "text/plain") =>
        new(_ =>
        {
            var response = new HttpResponseMessage(code)
            {
                Content = new StringContent(body, Encoding.UTF8, mediaType),
            };
            // Mimic the real API by echoing the request URI on the response message.
            response.RequestMessage = new HttpRequestMessage(HttpMethod.Get, "https://fake-api.example.com/v1/test");
            return response;
        });

    public static FakeHttpMessageHandler ReturnsJson(HttpStatusCode code, string json) =>
        Returns(code, json, "application/json");

    public static FakeHttpMessageHandler ReturnsHtml(HttpStatusCode code) =>
        Returns(code,
            "<!DOCTYPE html><html><head><title>Bad Gateway</title></head>" +
            "<body><h1>502 Bad Gateway</h1><p>nginx</p></body></html>",
            "text/html");

    public static FakeHttpMessageHandler ReturnsEmpty(HttpStatusCode code) =>
        new(_ =>
        {
            var response = new HttpResponseMessage(code) { Content = new StringContent("") };
            response.RequestMessage = new HttpRequestMessage(HttpMethod.Get, "https://fake-api.example.com/v1/test");
            return response;
        });
}

