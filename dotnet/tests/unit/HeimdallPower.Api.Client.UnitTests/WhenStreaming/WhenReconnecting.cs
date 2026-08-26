using HeimdallPower.Api.Client.Stream;
using HeimdallPower.Api.Client.UnitTests.WhenStreaming.Fakes;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming;

/// <summary>
/// Verifies <see cref="HeimdallStreamClient"/>'s transparent reconnection and cancellation behavior.
/// </summary>
[Trait("Category", "Unit")]
public class WhenReconnecting
{
    private static readonly StreamConnectionRetryPolicy ZeroDelay = new(TimeSpan.Zero, TimeSpan.Zero);

    private static HeimdallStreamClient CreateClient(HttpMessageHandler handler) =>
        new(new CountingAccessTokenProvider(),
            new HttpClient(handler) { BaseAddress = new Uri("https://fake-stream.example.com") },
            retryPolicy: ZeroDelay);

    [Fact]
    public async Task ShouldRecover_AfterTransientConnectionFailure()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();

        var callCount = 0;
        var handler = new CountingHttpMessageHandler(_ =>
        {
            callCount++;
            if (callCount == 1)
                throw new HttpRequestException("Connection refused");

            return SseTestData.OkResponse(SseTestData.DlrEvent(lineId, spanId, DateTimeOffset.UtcNow, 7.0));
        });

        var client = CreateClient(handler);
        using var cts = new CancellationTokenSource();
        var logMessages = new List<string>();

        HeimdallEventEnvelope? received = null;
        await foreach (var envelope in client.ReceiveAsync(gridOwnerId: null, infoLogger: logMessages.Add, cts.Token))
        {
            received = envelope;
            break;
        }

        Assert.NotNull(received);
        Assert.Equal(2, callCount);
        Assert.Contains(logMessages, m => m.Contains("Stream error", StringComparison.OrdinalIgnoreCase));
    }

    [Fact]
    public async Task ShouldContinueYieldingEvents_AcrossReconnectBoundary()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();

        var callCount = 0;
        var handler = new CountingHttpMessageHandler(_ =>
        {
            callCount++;
            // Each connect's canned body ends after one event, forcing a reconnect for the next.
            return SseTestData.OkResponse(SseTestData.DlrEvent(lineId, spanId, DateTimeOffset.UtcNow, callCount));
        });

        var client = CreateClient(handler);
        using var cts = new CancellationTokenSource();

        var values = new List<double>();
        await foreach (var envelope in client.ReceiveAsync(gridOwnerId: null, infoLogger: _ => { }, cts.Token))
        {
            values.Add(envelope.HeimdallDlr!.Value);
            if (values.Count == 3)
                break;
        }

        Assert.Equal([1.0, 2.0, 3.0], values);
    }

    [Fact]
    public async Task ShouldStopCleanly_WhenCancellationRequested()
    {
        var handler = new CountingHttpMessageHandler(_ => SseTestData.OkResponseNeverEnding(SseTestData.HeartbeatEvent));
        var client = CreateClient(handler);

        using var cts = new CancellationTokenSource();
        var events = new List<HeimdallEventEnvelope>();

        var enumerationTask = Task.Run(async () =>
        {
            await foreach (var envelope in client.ReceiveAsync(gridOwnerId: null, infoLogger: _ => { }, cts.Token))
            {
                events.Add(envelope);
            }
        });

        cts.CancelAfter(TimeSpan.FromMilliseconds(100));

        // Should complete (not throw) once cancelled - no exception surfaces to the caller.
        await enumerationTask;

        Assert.Empty(events);
    }
}
