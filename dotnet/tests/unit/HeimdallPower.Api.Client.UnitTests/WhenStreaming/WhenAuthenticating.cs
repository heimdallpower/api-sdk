using HeimdallPower.Api.Client.Stream;
using HeimdallPower.Api.Client.UnitTests.WhenStreaming.Fakes;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming;

/// <summary>
/// Verifies that <see cref="HeimdallStreamClient"/> acquires, reuses, and refreshes its access
/// token correctly - no network calls, no real MSAL/AAD.
/// </summary>
[Trait("Category", "Unit")]
public class WhenAuthenticating
{
    private static readonly StreamConnectionRetryPolicy ZeroDelay = new(new StreamConnectionRetryPolicyOptions { InitialDelay = TimeSpan.Zero, MaxDelay = TimeSpan.Zero });

    [Fact]
    public async Task ShouldAttachAuthAndClientHeaders_BeforeFirstConnect()
    {
        HttpRequestMessage? capturedRequest = null;
        var handler = new CountingHttpMessageHandler(request =>
        {
            capturedRequest = request;
            return SseTestData.OkResponse(SseTestData.DlrEvent(Guid.NewGuid(), Guid.NewGuid(), DateTimeOffset.UtcNow, 1.0));
        });

        var client = new HeimdallStreamClient(
            new CountingAccessTokenProvider(),
            new HttpClient(handler) { BaseAddress = new Uri("https://fake-stream.example.com") },
            retryPolicy: ZeroDelay);

        using var cts = new CancellationTokenSource();
        await foreach (var _ in client.ReceiveAsync(infoLogger: _ => { }, token: cts.Token))
        {
            break;
        }

        Assert.NotNull(capturedRequest);
        Assert.True(capturedRequest!.Headers.Contains("Authorization"));
        Assert.True(capturedRequest.Headers.Contains("x-region"));
        Assert.True(capturedRequest.Headers.Contains("x-client-name"));
        Assert.True(capturedRequest.Headers.Contains("x-client-version"));
    }

    [Fact]
    public async Task ShouldReuseToken_AcrossReconnects_WhileStillFresh()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();
        var handler = new CountingHttpMessageHandler(_ =>
            SseTestData.OkResponse(SseTestData.DlrEvent(lineId, spanId, DateTimeOffset.UtcNow, 1.0)));

        var tokenProvider = new CountingAccessTokenProvider(expiresOn: DateTimeOffset.UtcNow.AddHours(1));
        var client = new HeimdallStreamClient(
            tokenProvider,
            new HttpClient(handler) { BaseAddress = new Uri("https://fake-stream.example.com") },
            retryPolicy: ZeroDelay);

        using var cts = new CancellationTokenSource();
        var receivedCount = 0;
        await foreach (var _ in client.ReceiveAsync(infoLogger: _ => { }, token: cts.Token))
        {
            receivedCount++;
            if (receivedCount == 2)
                break; // Received one event from each of two connects (server closes after each canned response).
        }

        Assert.Equal(2, receivedCount);
        Assert.Equal(1, tokenProvider.AcquireTokenCallCount);
    }

    [Fact]
    public async Task ShouldForceRefreshToken_OnUnauthorizedResponse()
    {
        var lineId = Guid.NewGuid();
        var spanId = Guid.NewGuid();

        var callCount = 0;
        var handler = new CountingHttpMessageHandler(_ =>
        {
            callCount++;
            return callCount == 1
                ? new HttpResponseMessage(System.Net.HttpStatusCode.Unauthorized)
                : SseTestData.OkResponse(SseTestData.DlrEvent(lineId, spanId, DateTimeOffset.UtcNow, 1.0));
        });

        var tokenProvider = new CountingAccessTokenProvider();
        var client = new HeimdallStreamClient(
            tokenProvider,
            new HttpClient(handler) { BaseAddress = new Uri("https://fake-stream.example.com") },
            retryPolicy: ZeroDelay);

        using var cts = new CancellationTokenSource();
        var logMessages = new List<string>();

        HeimdallEventEnvelope? received = null;
        await foreach (var envelope in client.ReceiveAsync(infoLogger: logMessages.Add, token: cts.Token))
        {
            received = envelope;
            break;
        }

        Assert.NotNull(received);
        Assert.Equal(2, callCount);
        Assert.Equal(2, tokenProvider.AcquireTokenCallCount); // Initial acquire + forced refresh after the 401.
        Assert.Contains(logMessages, m => m.Contains("unauthorized", StringComparison.OrdinalIgnoreCase));
    }
}
