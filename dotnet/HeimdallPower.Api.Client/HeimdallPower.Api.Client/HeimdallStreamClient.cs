using System.Net.ServerSentEvents;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace HeimdallPower.Api.Client;

public class HeimdallStreamClient(HttpClient httpClient) : IHeimdallStreamClient
{
    private static readonly TimeSpan InitialRetryDelay = TimeSpan.FromSeconds(1);
    private static readonly TimeSpan MaxRetryDelay = TimeSpan.FromSeconds(30);

    private static readonly string AssemblyVersion = Assembly.GetExecutingAssembly().GetName().Version?.ToString() ?? "0.0.0";
    private const string ClientName = "dotnet-sdk";


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

        // Do as the api sdk does
        httpClient.DefaultRequestHeaders.TryAddWithoutValidation("x-client-name", ClientName);
        httpClient.DefaultRequestHeaders.TryAddWithoutValidation("x-client-version", AssemblyVersion);

        while (!token.IsCancellationRequested)
        {
            // The inner iterator is driven manually so that try/catch can wrap MoveNextAsync
            // without ever wrapping a yield return (which the compiler forbids).
            await using var enumerator = ConnectAndReadAsync(gridOwnerId, httpClient, infoLogger, token)
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
                await Task.Delay(GetRetryDelay(failedAttempts), token);
            }
            catch (OperationCanceledException)
            {
                yield break;
            }
        }
    }

    private static async IAsyncEnumerable<HeimdallEventEnvelope> ConnectAndReadAsync(
        Guid? gridOwnerId,
        HttpClient httpClient,
        Action<string> infoLogger,
        [EnumeratorCancellation] CancellationToken token)
    {
        using var request = new HttpRequestMessage(
                                    HttpMethod.Get,
                                    $"/v1/stream?gridownerid={gridOwnerId}");

        using var response = await httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead, token);
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

            if (item.EventType == HeimdallDlr.MetricName)
            {
                HeimdallEventEnvelope? envelope = JsonSerializer.Deserialize<HeimdallEventEnvelope>(item.Data, HeimdallJsonSerializerOptions.Default);

                if (envelope is null)
                    continue;

                yield return envelope;
            }
        }
    }

    private static TimeSpan GetRetryDelay(int failedAttempts)
    {
        if (failedAttempts <= 0)
            return InitialRetryDelay;

        var exponential = InitialRetryDelay * Math.Pow(2, Math.Min(failedAttempts, 10));
        var capped = exponential < MaxRetryDelay ? exponential : MaxRetryDelay;

        // Jitter avoids a thundering herd of clients reconnecting simultaneously.
        return capped * (0.8 + (Random.Shared.NextDouble() * 0.4));
    }
}



public record HeimdallEventEnvelope(
    string SchemaVersion,
    string Metric,
    string Unit,
    JsonElement Data)
{
    private HeimdallDlr? _heimdallDlr;

    public HeimdallDlr? HeimdallDlr
    {
        get
        {
            return _heimdallDlr ??= Data.Deserialize<HeimdallDlr>(HeimdallJsonSerializerOptions.Default);
        }
    }
}

public record HeimdallDlr(
    Guid AtLineId,
    Guid AtSpanId,
    DateTimeOffset Timestamp,
    double Value,
    bool IsFallback)
{
    public const string MetricName = "Heimdall DLR";
}

public static class HeimdallJsonSerializerOptions
{
    private static JsonSerializerOptions? _jsonOptions;

    private static JsonSerializerOptions CreateJsonOptions()
    {
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
        };
        options.Converters.Add(new JsonStringEnumConverter());
        return options;
    }

    public static JsonSerializerOptions Default
    {
        get
        {
            return _jsonOptions ??= CreateJsonOptions();
        }
    }
}
