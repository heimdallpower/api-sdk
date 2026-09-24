namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional data to include in a conductor temperature response, in addition to the line-level aggregate.
/// </summary>
public enum ConductorTemperatureInclude
{
    /// <summary>
    /// Additionally include a per-measurement-point breakdown of conductor temperature (as unaggregated data),
    /// organized by span and span phase. Sent as <c>include=measurement_points</c>.
    /// </summary>
    MeasurementPoints,
}

internal static class ConductorTemperatureIncludeExtensions
{
    public static string ToQueryValue(this ConductorTemperatureInclude include) => include switch
    {
        ConductorTemperatureInclude.MeasurementPoints => "measurement_points",
        _ => throw new ArgumentOutOfRangeException(nameof(include), include, "Unsupported include value."),
    };
}
