using HeimdallPower.Api.Client;
using HeimdallPower.Api.Client.Stream.CapacityMonitoring;
using HeimdallPower.Api.Client.Stream.CapacityMonitoring.Lines;
using System.Net;
using System.Net.ServerSentEvents;
using System.Runtime.CompilerServices;
using System.Text.Json;

namespace HeimdallPower.Api.Client.Stream;

/// <summary>
/// Default <see cref="IHeimdallStreamClient"/> implementation, backed by an <see cref="HttpClient"/> that
/// consumes the Heimdall Stream API's Server-Sent Events endpoint.
/// </summary>
public class HeimdallStreamClient : IHeimdallStreamClient
{
    private readonly HttpClient _httpClient;
    private readonly AccessTokenHeaderRefresher _tokenRefresher;
    private readonly StreamConnectionRetryPolicy _retryPolicy;

    /// <summary>
    /// A client that lets you consume the Heimdall Stream API.
    /// </summary>
    /// <remarks>
    /// This client will automatically attempt to reconnect with exponential backoff when transient errors occur.
    /// The number of retry attempts is determined by the <see cref="StreamConnectionRetryPolicyOptions"/>.
    /// </remarks>
    /// <param name="clientId">The client ID used to authenticate with the Heimdall Power API.</param>
    /// <param name="clientSecret">The client secret used to authenticate with the Heimdall Power API.</param>
    /// <param name="httpClient">An optional pre-configured <see cref="HttpClient"/>. When omitted, one is created with the default stream base address.</param>
    /// <param name="clientMetadata">Optional additional metadata to include in request headers.</param>
    /// <param name="proxyHandler">An optional message handler used to route token acquisition through a proxy.</param>
    /// <param name="retryPolicyOptions">Optional configuration for the reconnect backoff behavior.</param>
    public HeimdallStreamClient(string clientId, string clientSecret, HttpClient? httpClient = null, Dictionary<string, string>? clientMetadata = null, HttpMessageHandler? proxyHandler = null, StreamConnectionRetryPolicyOptions? retryPolicyOptions = null)
        : this(
            new AccessTokenProvider(clientId, clientSecret, HeimdallApiEndpoints.Authority, HeimdallApiEndpoints.Scope, proxyHandler),
            httpClient ?? new HttpClient { BaseAddress = new Uri(HeimdallApiEndpoints.StreamUrl) },
            clientMetadata,
            new StreamConnectionRetryPolicy(retryPolicyOptions))
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
    /// Streams events for the specified grid owner with the specified quantity, transparently reconnecting with exponential backoff when the
    /// connection drops or fails. The consumer only ever sees a continuous sequence of events. All event types are returned in a single stream, and the consumer can filter them by type if desired.
    /// The stream runs until the provided cancellation token is cancelled, or an unrecoverable error occurs.
    /// </summary>
    /// <throws cref="HeimdallApiException">Thrown on non-transient errors after exhausting all retry attempts.</throws>
    /// <param name="gridOwnerId">The grid owner to receive events for, or <see langword="null"/> to receive events for the authenticated grid owner.</param>
    /// <param name="quantity">The physical quantity to receive events for, Current (default) or ApparentPower.</param>
    /// <param name="infoLogger">Callback invoked with diagnostic messages (e.g. errors, reconnect attempts), or <see langword="null"/> if no logging is desired. Not used for any event data.</param>
    /// <param name="traceLogger">Callback invoked with trace messages (e.g. heartbeats, received events), or <see langword="null"/> if no logging is desired. Does not log the detailed event data.</param>
    /// <param name="token">A token used to stop receiving events and end the stream.</param>
    /// <returns>An asynchronous stream of <see cref="HeimdallEventEnvelope"/> that runs until cancelled.</returns>
    public async IAsyncEnumerable<HeimdallEventEnvelope> ReceiveAsync(
        Guid? gridOwnerId,
        Quantity quantity = Quantity.Current,
        Action<string>? infoLogger = null,
        Action<string>? traceLogger = null,
        [EnumeratorCancellation] CancellationToken token = default)
    {
        var failedAttempts = 0;
        infoLogger?.Invoke("Starting Heimdall stream...");

        while (!token.IsCancellationRequested)
        {
            // The inner iterator is driven manually so that try/catch can wrap MoveNextAsync
            // without ever wrapping a yield return (which the compiler forbids).
            await using var enumerator = ConnectAndReadAsync(gridOwnerId, quantity, traceLogger, token)
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
                    infoLogger?.Invoke($"Stream error: unauthorized. Refreshing token and reconnecting... (attempt #{failedAttempts})");
                    await _tokenRefresher.ForceRefreshAsync(token);
                    break;
                }
                catch (Exception ex)
                {
                    failedAttempts++;

                    if (ex is HeimdallApiException
                    && !_retryPolicy.ShouldRetry(failedAttempts)) 
                        throw;

                    infoLogger?.Invoke($"Stream error: {ex.Message}. Reconnecting... (attempt #{failedAttempts})");
                    break;
                }

                yield return envelope;
            }

            if (token.IsCancellationRequested)
                yield break;

            try
            {
                if (_retryPolicy.ShouldRetry(failedAttempts))
                {
                    await Task.Delay(_retryPolicy.GetDelay(failedAttempts), token);
                }
                else
                {
                    infoLogger?.Invoke($"Stream error: exceeded maximum retry attempts ({failedAttempts}). Stopping stream.");
                    yield break;
                }
            }
            catch (OperationCanceledException)
            {
                yield break;
            }
        }
    }

    /// <summary>
    /// Opens a single SSE connection and yields the events read from it until the connection ends or fails.
    /// Does not reconnect; that is handled by the caller, <see cref="ReceiveAsync"/>.
    /// </summary>
    private async IAsyncEnumerable<HeimdallEventEnvelope> ConnectAndReadAsync(
        Guid? gridOwnerId,
        Quantity quantity,
        Action<string>? traceLogger,
        [EnumeratorCancellation] CancellationToken token)
    {
        await _tokenRefresher.EnsureFreshTokenAsync(token);

        string url = UrlBuilder.BuildStreamUrl(version: 1, gridOwnerId, quantity);

        using var request = new HttpRequestMessage(
                                    HttpMethod.Get,
                                    url);

        using var response = await _httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead, token);

        if (response.StatusCode == HttpStatusCode.Unauthorized)
            throw new UnauthorizedAccessException("Unauthorized access. Please check your credentials.");

        if (!response.IsSuccessStatusCode)
        {
            var requestUrl = response.RequestMessage?.RequestUri?.ToString() ?? string.Empty;
            throw new HeimdallApiException(
                $"Stream request failed with status code {(int)response.StatusCode} {response.StatusCode}.",
                response.StatusCode,
                requestUrl);
        }

        await using var stream = await response.Content.ReadAsStreamAsync(token);

        await foreach (SseItem<string> item in SseParser.Create(stream).EnumerateAsync(token))
        {
            if (item.EventType == "heartbeat")
            {
                traceLogger?.Invoke("Heartbeat received.");
                continue;
            }

            if (string.IsNullOrWhiteSpace(item.Data))
                continue;

            if (item.EventType == HeimdallDlrEvent.EventName)
            {
                HeimdallEventEnvelope? envelope = JsonSerializer.Deserialize<HeimdallEventEnvelope>(item.Data, HeimdallStreamJsonSerializerOptions.Default);

                if (envelope is null)
                    continue;

                traceLogger?.Invoke("Received event: " + envelope.Metric);
                yield return envelope;
            }
        }
    }
}
