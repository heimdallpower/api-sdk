using System.Net;
using System.Net.ServerSentEvents;
using System.Runtime.CompilerServices;
using System.Text.Json;

namespace HeimdallPower.Api.Client.Stream;

public class HeimdallStreamClient : IHeimdallStreamClient
{
    private readonly HttpClient _httpClient;
    private readonly AccessTokenHeaderRefresher _tokenRefresher;
    private readonly StreamConnectionRetryPolicy _retryPolicy;

    /// <summary>
    /// A client that lets you consume the Heimdall Stream API.
    /// Throws <see cref="HeimdallApiException"/> on non-transient errors.
    /// </summary>
    public HeimdallStreamClient(string clientId, string clientSecret, HttpClient? httpClient = null, Dictionary<string, string>? clientMetadata = null, HttpMessageHandler? proxyHandler = null)
        : this(
            new AccessTokenProvider(clientId, clientSecret, HeimdallApiEndpoints.Authority, HeimdallApiEndpoints.Scope, proxyHandler),
            httpClient ?? new HttpClient { BaseAddress = new Uri(HeimdallApiEndpoints.ApiUrl) },
            clientMetadata)
    {
    }

    // Seam for unit tests to inject a stub IAccessTokenProvider and a zero-delay retry policy instead of hitting real MSAL/AAD and real backoff delays.
    internal HeimdallStreamClient(IAccessTokenProvider accessTokenProvider, HttpClient httpClient, Dictionary<string, string>? clientMetadata = null, StreamConnectionRetryPolicy? retryPolicy = null)
    {
        _httpClient = httpClient;
        _tokenRefresher = new AccessTokenHeaderRefresher(accessTokenProvider, httpClient, clientMetadata);
        _retryPolicy = retryPolicy ?? new StreamConnectionRetryPolicy();
    }

    /// <summary>
    /// Streams events, transparently reconnecting with exponential backoff when the
    /// connection drops or fails. The consumer only ever sees a continuous sequence of events.
    /// </summary>
    public async IAsyncEnumerable<HeimdallEventEnvelope> ReceiveAsync(
        Guid? gridOwnerId,
        Action<string> infoLogger,
        [EnumeratorCancellation] CancellationToken token)
    {
        var failedAttempts = 0;

        while (!token.IsCancellationRequested)
        {
            // The inner iterator is driven manually so that try/catch can wrap MoveNextAsync
            // without ever wrapping a yield return (which the compiler forbids).
            await using var enumerator = ConnectAndReadAsync(gridOwnerId, infoLogger, token)
                                                .GetAsyncEnumerator(token);

            while (true)
            {
                HeimdallEventEnvelope envelope;

                try
                {
                    if (!await enumerator.MoveNextAsync())
                        break; // Stream closed by server - reconnect.

                    envelope = enumerator.Current;
                    failedAttempts = 0; // A successful read resets the backoff.
                }
                catch (OperationCanceledException) when (token.IsCancellationRequested)
                {
                    yield break;
                }
                catch (UnauthorizedAccessException)
                {
                    failedAttempts++;
                    infoLogger($"Stream error: unauthorized. Refreshing token and reconnecting... (attempt #{failedAttempts})");
                    await _tokenRefresher.ForceRefreshAsync(token);
                    break;
                }
                catch (Exception ex)
                {
                    failedAttempts++;
                    infoLogger($"Stream error: {ex.Message}. Reconnecting... (attempt #{failedAttempts})");
                    break;
                }

                yield return envelope;
            }

            if (token.IsCancellationRequested)
                yield break;

            try
            {
                // Should we break the loop after a number of failed attempts?
                await Task.Delay(_retryPolicy.GetDelay(failedAttempts), token);
            }
            catch (OperationCanceledException)
            {
                yield break;
            }
        }
    }

    private async IAsyncEnumerable<HeimdallEventEnvelope> ConnectAndReadAsync(
        Guid? gridOwnerId,
        Action<string> infoLogger,
        [EnumeratorCancellation] CancellationToken token)
    {
        await _tokenRefresher.EnsureFreshTokenAsync(token);

        using var request = new HttpRequestMessage(
                                    HttpMethod.Get,
                                    $"/v1/stream?gridownerid={gridOwnerId}");

        using var response = await _httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead, token);

        if (response.StatusCode == HttpStatusCode.Unauthorized)
            throw new UnauthorizedAccessException("Unauthorized access. Please check your credentials.");

        response.EnsureSuccessStatusCode();

        await using var stream = await response.Content.ReadAsStreamAsync(token);

        await foreach (SseItem<string> item in SseParser.Create(stream).EnumerateAsync(token))
        {
            if (item.EventType == "heartbeat")
            {
                infoLogger("Heartbeat received..");// This is debug information, should check if the user wants to log it or not
                continue;
            }

            if (string.IsNullOrWhiteSpace(item.Data))
                continue;

            if (item.EventType == HeimdallDlrEvent.MetricName)
            {
                HeimdallEventEnvelope? envelope = JsonSerializer.Deserialize<HeimdallEventEnvelope>(item.Data, HeimdallStreamJsonSerializerOptions.Default);

                if (envelope is null)
                    continue;

                yield return envelope;
            }
        }
    }
}
