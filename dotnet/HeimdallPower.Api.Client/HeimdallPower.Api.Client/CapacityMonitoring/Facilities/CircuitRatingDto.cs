namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

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
