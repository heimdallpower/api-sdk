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
    /// <param name="gridOwnerId">The grid owner to receive events for, or <see langword="null"/> to receive events for all grid owners accessible to the authenticated client.</param>
    /// <param name="infoLogger">Callback invoked with diagnostic messages (e.g. heartbeats, reconnect attempts). Not used for the actual event data.</param>
    /// <param name="token">A token used to stop receiving events and end the stream.</param>
    /// <returns>An asynchronous stream of Heimdall event envelopes that runs until cancelled.</returns>
    IAsyncEnumerable<HeimdallEventEnvelope> ReceiveAsync(Guid? gridOwnerId, Action<string> infoLogger, CancellationToken token);
}
