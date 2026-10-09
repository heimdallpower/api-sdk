namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetHeimdallDlrsAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetHeimdallDlrsOptions
{
    /// <summary>
    /// The quantity to return. Defaults to <see cref="CapacityMonitoring.Quantity.Current"/> (amperes); use <see cref="CapacityMonitoring.Quantity.ApparentPower"/> for MVA.
    /// </summary>
    public Quantity Quantity { get; init; } = Quantity.Current;

    /// <summary>
    /// Set to <see cref="HeimdallDlrInclude.Spans"/> to additionally include a per-span breakdown of Heimdall DLR over the requested time range. Omitted by default.
    /// When set, the requested period must not exceed 7 days.
    /// </summary>
    public HeimdallDlrInclude? Include { get; init; }
}
