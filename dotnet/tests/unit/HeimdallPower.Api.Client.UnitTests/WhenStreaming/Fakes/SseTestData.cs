using System.Net;
using System.Text;
using System.Text.Json;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming.Fakes;

/// <summary>
/// Builds canned SSE (text/event-stream) response bodies and HTTP responses for stream client tests.
/// </summary>
internal static class SseTestData
{
    public static string HeartbeatEvent => "event: heartbeat\ndata: \n\n";

    public static string DlrEvent(Guid lineId, Guid spanId, DateTimeOffset timestamp, double value, bool isFallback = false)
    {
        var payload = new
        {
            schema_version = "1.0",
            metric = "Heimdall DLR",
            unit = "Ampere",
            data = new { at_line_id = lineId, at_span_id = spanId, timestamp, value, is_fallback = isFallback },
        };
        var json = JsonSerializer.Serialize(payload);
        return $"event: Heimdall DLR\ndata: {json}\n\n";
    }

    public static string UnknownEvent => "event: something_else\ndata: {\"foo\":\"bar\"}\n\n";

    public static string MalformedDlrEvent => "event: Heimdall DLR\ndata: not-json\n\n";

    public static HttpResponseMessage OkResponse(string sseBody) => new(HttpStatusCode.OK)
    {
        Content = new StringContent(sseBody, Encoding.UTF8, "text/event-stream"),
    };

    public static HttpResponseMessage OkResponseNeverEnding(string initialSseBody) => new(HttpStatusCode.OK)
    {
        Content = new StreamContent(new NeverEndingSseStream(initialSseBody))
        {
            Headers = { ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("text/event-stream") },
        },
    };
}
