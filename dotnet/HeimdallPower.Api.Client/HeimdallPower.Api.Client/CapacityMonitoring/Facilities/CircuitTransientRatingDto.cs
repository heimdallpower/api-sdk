namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

/// <summary>
/// The circuit transient rating is the line transient rating capped, per duration, by the most-limiting facility
/// component's emergency rating. It is the short-duration overload equivalent of the circuit rating and is a set of
/// per-duration values calculated at a single point in time.
/// </summary>
public record CircuitTransientRatingDto
{
    /// <summary>
    /// Time (in UTC) when the circuit transient rating was calculated.
    /// </summary>
    /// <example>2024-07-01T12:00:00.001Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The circuit transient rating for each calculated duration at the given timestamp. Ordered by duration ascending.
    /// </summary>
    public required List<CircuitTransientRatingValueDto> Ratings { get; init; }
}
