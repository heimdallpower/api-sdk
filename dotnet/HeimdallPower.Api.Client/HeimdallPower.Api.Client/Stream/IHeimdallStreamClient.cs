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
    /// Receives Heimdall events from the Heimdall Stream API as an asynchronous stream.
    /// </summary>
    /// <param name="gridOwnerId">The ID of the grid owner.</param>
    /// <param name="infoLogger">A logger action for informational messages.</param>
    /// <param name="token">A cancellation token.</param>
    /// <returns>An asynchronous stream of Heimdall event envelopes.</returns>
    IAsyncEnumerable<HeimdallEventEnvelope> ReceiveAsync(Guid? gridOwnerId, Action<string> infoLogger, CancellationToken token);
}
