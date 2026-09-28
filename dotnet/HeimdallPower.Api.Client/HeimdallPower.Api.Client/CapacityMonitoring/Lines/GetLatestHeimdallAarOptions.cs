namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetLatestHeimdallAarAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetLatestHeimdallAarOptions
{
    /// <summary>
    /// The quantity to return. Defaults to <see cref="CapacityMonitoring.Quantity.Current"/> (amperes); use <see cref="CapacityMonitoring.Quantity.ApparentPower"/> for MVA.
    /// </summary>
    public Quantity Quantity { get; init; } = Quantity.Current;

    /// <summary>
    /// Optional cut-off time (UTC). If the latest Heimdall AAR is older than this value, the API returns 404 Not Found.
    /// </summary>
    public DateTimeOffset? Since { get; init; }
}
