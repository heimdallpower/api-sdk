namespace HeimdallPower.Api.Client;

/// <summary>
/// Interface for a Heimdall stream client that receives events from the Heimdall Stream API.
/// </summary>
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
