namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional data to include in a current response, in addition to the line-level aggregate.
/// </summary>
public enum CurrentInclude
{
    /// <summary>
    /// Additionally include a per-measurement-point breakdown of current (as unaggregated data),
    /// organized by span and span phase. Sent as <c>include=measurement_points</c>.
    /// </summary>
    MeasurementPoints,
}

internal static class CurrentIncludeExtensions
{
    public static string ToQueryValue(this CurrentInclude include) => include switch
    {
        CurrentInclude.MeasurementPoints => "measurement_points",
        _ => throw new ArgumentOutOfRangeException(nameof(include), include, "Unsupported include value."),
    };
}
