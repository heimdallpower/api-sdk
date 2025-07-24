namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

/// <summary>
/// The circuit rating is defined as the lowest of either Heimdall DLR, lowest steady-state rating among all facility components, or the facility's upper limit.
/// The upper limit can be either a fixed value or a percentage of the line's steady-state rating.
/// </summary>
public record CircuitRatingDto
{
    /// <summary>
    /// Time (in UTC) when the circuit rating was.
    /// </summary>
    /// <example>2024-07-01T12:00:00.001Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The measured circuit rating value.
    /// </summary>
    /// <example>375.4</example>
    public double Value { get; init; }
}
