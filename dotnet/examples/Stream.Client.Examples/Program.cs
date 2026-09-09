using HeimdallPower.Api.Client.Stream;
using HeimdallPower.Api.Client.Stream.CapacityMonitoring;

// Configuration setup
string clientId = Environment.GetEnvironmentVariable("HP_CLIENT_ID") ?? throw new InvalidOperationException("HP_CLIENT_ID environment variable is not set.");
string clientSecret = Environment.GetEnvironmentVariable("HP_CLIENT_SECRET") ?? throw new InvalidOperationException("HP_CLIENT_SECRET environment variable is not set.");

Console.WriteLine("Initiating Heimdall Stream client");

// Note: direct instantiation does NOT include automatic HTTP resilience.
// Reconnection with backoff for dropped/failed connections is handled internally by HeimdallStreamClient.
var streamClient = new HeimdallStreamClient(clientId, clientSecret);

using var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) =>
{
    e.Cancel = true; // Let the loop below exit gracefully instead of killing the process immediately.
    cts.Cancel();
};

Console.WriteLine("Listening for events. Press Ctrl+C to stop.");

await foreach (var envelope in streamClient.ReceiveAsync(quantity: Quantity.Current, infoLogger: Console.WriteLine, traceLogger: Console.WriteLine, token: cts.Token))
{
    if (envelope.HeimdallDlr is { } dlr)
    {
        Console.WriteLine($"- Heimdall DLR: {dlr.Value} {envelope.Unit} for line {dlr.AtLineId} at {dlr.Timestamp} (IsFallback={dlr.IsFallback})");
    }
    else
    {
        Console.WriteLine($"- {envelope.Metric}: {envelope.Data}");
    }
}

Console.WriteLine("Stream stopped.");
