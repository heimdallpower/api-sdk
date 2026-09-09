using HeimdallPower.Api.Client.Common;
using HeimdallPower.Api.Client.REST;

namespace HeimdallPower.Api.Client.Stream;

/// <summary>
/// Interface for a Heimdall stream client that receives events from the Heimdall Stream API.
/// </summary>
/// <remarks>
/// <b>Authentication:</b> handled internally. The token is acquired and refreshed automatically
/// before connecting and after an unauthorized (401) response, using the same client credentials
/// flow as <see cref="IHeimdallApiClient"/>.
/// <para>
/// <b>Reconnection:</b> connection drops and transient failures are retried internally with
/// exponential backoff. Callers only ever see a continuous sequence of events.
/// </para>
/// </remarks>
public interface IHeimdallStreamClient
{
    /// <summary>
    /// Receives Heimdall events from the Heimdall Stream API as a continuous asynchronous stream.
    /// </summary>
    /// <remarks>
    /// The returned sequence does not complete on its own: it keeps yielding events, transparently
    /// reconnecting behind the scenes, until <paramref name="token"/> is cancelled. Cancelling the
    /// token ends enumeration gracefully rather than throwing.
    /// </remarks>
    /// <param name="quantity">The physical quantity to receive events for, Current (default) or ApparentPower.</param>
    /// <param name="infoLogger">Callback invoked with diagnostic messages (e.g. errors, reconnect attempts), or <see langword="null"/> if no logging is desired. Not used for any event data.</param>
    /// <param name="traceLogger">Callback invoked with trace messages (e.g. heartbeats, received events), or <see langword="null"/> if no logging is desired. Does not log the detailed event data.</param>
    /// <param name="token">A token used to stop receiving events and end the stream.</param>
    /// <returns>An asynchronous stream of Heimdall event envelopes that runs until cancelled.</returns>
    IAsyncEnumerable<HeimdallEventEnvelope> ReceiveAsync(Quantity quantity = Quantity.Current, Action<string>? infoLogger = null, Action<string>? traceLogger = null, CancellationToken token = default);
}
