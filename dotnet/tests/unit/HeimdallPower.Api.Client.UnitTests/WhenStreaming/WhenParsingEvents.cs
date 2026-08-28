using HeimdallPower.Api.Client.Stream;
using HeimdallPower.Api.Client.UnitTests.WhenStreaming.Fakes;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming;

/// <summary>
/// Verifies SSE event parsing behavior of <see cref="HeimdallStreamClient"/> - no network calls, no auth.
/// </summary>
[Trait("Category", "Unit")]
public class WhenParsingEvents
{
    private static HeimdallStreamClient CreateClient(HttpMessageHandler handler) =>
        new(new CountingAccessTokenProvider(),
            new HttpClient(handler) { BaseAddress = new Uri("https://fake-stream.example.com") },
            retryPolicy: new StreamConnectionRetryPolicy(new StreamConnectionRetryPolicyOptions { InitialDelay = TimeSpan.Zero, MaxDelay = TimeSpan.Zero }));

    [Fact]
    public async Task ShouldYieldDeserializedDlrEvent_ForHeimdallDlrEventType()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();
        var timestamp = new DateTimeOffset(2026, 1, 1, 12, 0, 0, TimeSpan.Zero);

        var handler = new CountingHttpMessageHandler(_ =>
            SseTestData.OkResponse(SseTestData.DlrEvent(lineId, spanId, timestamp, 123.4)));

        var client = CreateClient(handler);
        using var cts = new CancellationTokenSource();

        HeimdallEventEnvelope? received = null;
        await foreach (var envelope in client.ReceiveAsync(gridOwnerId: null, infoLogger: _ => { }, token: cts.Token))
        {
            received = envelope;
            break;
        }

        Assert.NotNull(received);
        Assert.Equal("Heimdall DLR", received!.Metric);
        Assert.NotNull(received.HeimdallDlr);
        Assert.Equal(lineId, received.HeimdallDlr!.AtLineId);
        Assert.Equal(spanId, received.HeimdallDlr.AtSpanId);
        Assert.Equal(123.4, received.HeimdallDlr.Value);
        Assert.Equal(timestamp, received.HeimdallDlr.Timestamp);
        Assert.False(received.HeimdallDlr.IsFallback);
    }

    [Fact]
    public async Task ShouldNotYieldHeartbeats_ButShouldLogThem()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();
        var body = SseTestData.HeartbeatEvent + SseTestData.DlrEvent(lineId, spanId, DateTimeOffset.UtcNow, 1.0);

        var handler = new CountingHttpMessageHandler(_ => SseTestData.OkResponse(body));
        var client = CreateClient(handler);
        using var cts = new CancellationTokenSource();
        var logMessages = new List<string>();
        var traceMessages = new List<string>();

        var events = new List<HeimdallEventEnvelope>();
        await foreach (var envelope in client.ReceiveAsync(gridOwnerId: null, infoLogger: logMessages.Add, traceLogger: traceMessages.Add, token: cts.Token))
        {
            events.Add(envelope);
            break;
        }

        Assert.Single(events);
        Assert.Contains(traceMessages, m => m.Contains("Heartbeat", StringComparison.OrdinalIgnoreCase));
    }

    [Fact]
    public async Task ShouldSkipUnknownEventTypes()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();
        var body = SseTestData.UnknownEvent + SseTestData.DlrEvent(lineId, spanId, DateTimeOffset.UtcNow, 1.0);

        var handler = new CountingHttpMessageHandler(_ => SseTestData.OkResponse(body));
        var client = CreateClient(handler);
        using var cts = new CancellationTokenSource();

        var events = new List<HeimdallEventEnvelope>();
        await foreach (var envelope in client.ReceiveAsync(gridOwnerId: null, infoLogger: _ => { }, token: cts.Token))
        {
            events.Add(envelope);
            break;
        }

        Assert.Single(events);
        Assert.Equal("Heimdall DLR", events[0].Metric);
    }

    [Fact]
    public async Task ShouldRecoverAndReconnect_WhenDataIsMalformed()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();

        var callCount = 0;
        var handler = new CountingHttpMessageHandler(_ =>
        {
            callCount++;
            return callCount == 1
                ? SseTestData.OkResponse(SseTestData.MalformedDlrEvent)
                : SseTestData.OkResponse(SseTestData.DlrEvent(lineId, spanId, DateTimeOffset.UtcNow, 42.0));
        });

        var client = CreateClient(handler);
        using var cts = new CancellationTokenSource();
        var logMessages = new List<string>();

        HeimdallEventEnvelope? received = null;
        await foreach (var envelope in client.ReceiveAsync(gridOwnerId: null, infoLogger: logMessages.Add, token: cts.Token))
        {
            received = envelope;
            break;
        }

        Assert.NotNull(received);
        Assert.Equal(42.0, received!.HeimdallDlr!.Value);
        Assert.Contains(logMessages, m => m.Contains("Stream error", StringComparison.OrdinalIgnoreCase));
        Assert.Equal(2, callCount);
    }
}
