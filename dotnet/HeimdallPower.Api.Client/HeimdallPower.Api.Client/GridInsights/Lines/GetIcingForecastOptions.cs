namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetIcingForecastAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetIcingForecastOptions
{
    /// <summary>
    /// The unit system for the measurements. <see cref="Client.UnitSystem.Metric"/> uses kg/m, <see cref="Client.UnitSystem.Imperial"/> uses lb/ft. Defaults to metric.
    /// </summary>
    public UnitSystem UnitSystem { get; init; } = UnitSystem.Metric;
}
