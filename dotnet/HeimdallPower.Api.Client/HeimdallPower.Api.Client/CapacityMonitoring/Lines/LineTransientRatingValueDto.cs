namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

/// <summary>
/// The line transient rating for a single duration at a given timestamp.
/// </summary>
public record LineTransientRatingValueDto
{
    /// <summary>
    /// The transient rating duration in minutes. Transient ratings are not calculated for durations longer than one hour.
    /// </summary>
    /// <example>10</example>
    public int DurationMinutes { get; init; }

    /// <summary>
    /// The line transient rating value for this duration. The unit is given by the Unit property on the response:
    /// amperes for current (default), MVA for apparent power.
    /// </summary>
    /// <example>620.5</example>
    public double Value { get; init; }
}
