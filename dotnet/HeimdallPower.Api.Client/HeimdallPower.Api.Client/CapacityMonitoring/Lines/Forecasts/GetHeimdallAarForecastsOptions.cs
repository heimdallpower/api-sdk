namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetHeimdallAarForecastsAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetHeimdallAarForecastsOptions
{
    /// <summary>
    /// The quantity to return. Defaults to <see cref="CapacityMonitoring.Quantity.Current"/> (amperes); use <see cref="CapacityMonitoring.Quantity.ApparentPower"/> for MVA.
    /// </summary>
    public Quantity Quantity { get; init; } = Quantity.Current;
}
