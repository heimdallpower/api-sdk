namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetLatestSagAndClearanceAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetLatestSagAndClearanceOptions
{
    /// <summary>
    /// The unit system for the measurements. <see cref="Client.UnitSystem.Metric"/> uses kg/m, N and %; <see cref="Client.UnitSystem.Imperial"/> uses lb/ft, lbf and %. Defaults to metric.
    /// </summary>
    public UnitSystem UnitSystem { get; init; } = UnitSystem.Metric;

    /// <summary>
    /// Optional cut-off time (UTC). Only measurements at or after this instant are considered; older data for a span phase is excluded. If omitted, the API defaults to 30 minutes ago.
    /// </summary>
    public DateTimeOffset? Since { get; init; }
}
