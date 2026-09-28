namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetLatestConductorTemperatureAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetLatestConductorTemperatureOptions
{
    /// <summary>
    /// The unit system for response values. <see cref="Client.UnitSystem.Metric"/> gives Celsius (C), <see cref="Client.UnitSystem.Imperial"/> gives Fahrenheit (F). Defaults to metric.
    /// </summary>
    public UnitSystem UnitSystem { get; init; } = UnitSystem.Metric;

    /// <summary>
    /// Optional cut-off time (UTC). If the latest conductor temperature is older than this value, the API returns 404 Not Found.
    /// </summary>
    public DateTimeOffset? Since { get; init; }

    /// <summary>
    /// Set to <see cref="ConductorTemperatureInclude.MeasurementPoints"/> to additionally include a per-measurement-point breakdown of the latest conductor temperature, organized by span and span phase. Omitted by default.
    /// </summary>
    public ConductorTemperatureInclude? Include { get; init; }
}
