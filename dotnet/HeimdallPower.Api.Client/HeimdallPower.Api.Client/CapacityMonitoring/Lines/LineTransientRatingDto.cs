namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

/// <summary>
/// The line transient rating is the short-duration overload ampacity the line can sustain for each calculated duration.
/// It is a set of per-duration values calculated at a single point in time.
/// </summary>
public record LineTransientRatingDto
{
    /// <summary>
    /// Time (in UTC) when the line transient rating was calculated.
    /// </summary>
    /// <example>2024-07-01T12:00:00.001Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The line transient rating for each calculated duration at the given timestamp. Ordered by duration ascending.
    /// </summary>
    public required List<LineTransientRatingValueDto> Ratings { get; init; }
}
