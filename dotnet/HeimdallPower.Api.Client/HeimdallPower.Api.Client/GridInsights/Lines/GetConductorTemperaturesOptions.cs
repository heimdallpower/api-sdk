namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetConductorTemperaturesAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetConductorTemperaturesOptions
{
    /// <summary>
    /// The unit system for response values. <see cref="Client.UnitSystem.Metric"/> gives Celsius (C), <see cref="Client.UnitSystem.Imperial"/> gives Fahrenheit (F). Defaults to metric.
    /// </summary>
    public UnitSystem UnitSystem { get; init; } = UnitSystem.Metric;

    /// <summary>
    /// Set to <see cref="ConductorTemperatureInclude.MeasurementPoints"/> to additionally include a per-measurement-point breakdown of conductor temperature over the requested time range, organized by span and span phase. Omitted by default.
    /// </summary>
    public ConductorTemperatureInclude? Include { get; init; }
}
