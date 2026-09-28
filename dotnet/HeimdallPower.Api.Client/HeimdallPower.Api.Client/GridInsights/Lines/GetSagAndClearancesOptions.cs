namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetSagAndClearancesAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetSagAndClearancesOptions
{
    /// <summary>
    /// The unit system for the measurements. <see cref="Client.UnitSystem.Metric"/> uses kg/m, N and %; <see cref="Client.UnitSystem.Imperial"/> uses lb/ft, lbf and %. Defaults to metric.
    /// </summary>
    public UnitSystem UnitSystem { get; init; } = UnitSystem.Metric;
}
