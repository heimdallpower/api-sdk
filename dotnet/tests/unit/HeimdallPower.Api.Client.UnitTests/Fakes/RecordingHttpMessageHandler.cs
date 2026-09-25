using System.Net;
using System.Text;

namespace HeimdallPower.Api.Client.UnitTests.Fakes;

/// <summary>
/// An <see cref="HttpMessageHandler"/> that records every request it receives and answers
/// with a fixed JSON body, so tests can assert on the exact URL and query string the SDK sends.
/// </summary>
internal sealed class RecordingHttpMessageHandler(string json, HttpStatusCode statusCode = HttpStatusCode.OK) : HttpMessageHandler
{
    public List<HttpRequestMessage> Requests { get; } = [];

    public HttpRequestMessage LastRequest => Requests[^1];

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        Requests.Add(request);
        return Task.FromResult(new HttpResponseMessage(statusCode)
        {
            Content = new StringContent(json, Encoding.UTF8, "application/json"),
            RequestMessage = request,
        });
    }
}
