namespace HeimdallPower.Api.Client.Assets;

/// <summary>
/// Asset helpers for <see cref="IHeimdallApiClient"/>.
/// </summary>
public static class HeimdallApiClientAssetsExtensions
{
    /// <summary>
    /// Get the lines that have at least one active measurement point, with their facility and active measurement points.
    /// Use this instead of <see cref="IHeimdallApiClient.GetLinesAsync"/> when looping over lines to fetch data:
    /// lines with no measurement points, or only retired ones, return 404 or no data and are left out.
    /// </summary>
    /// <example>
    /// <code>
    /// foreach (var instrumented in await client.GetInstrumentedLinesAsync())
    /// {
    ///     var current = await client.GetLatestCurrentAsync(instrumented.Line.Id);
    ///     Console.WriteLine($"{instrumented.Facility.Name} / {instrumented.Line.Name}: {current.Current.Value} {current.Unit}");
    /// }
    /// </code>
    /// </example>
    /// <param name="client">The API client.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <returns>The instrumented lines. See <see cref="AssetsResponseExtensions.InstrumentedLines"/> for the selection rules.</returns>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    public static async Task<IReadOnlyList<InstrumentedLine>> GetInstrumentedLinesAsync(
        this IHeimdallApiClient client,
        CancellationToken cancellationToken = default)
    {
        ArgumentNullException.ThrowIfNull(client);
        var assets = await client.GetAssetsAsync(cancellationToken);
        return assets.InstrumentedLines();
    }
}
