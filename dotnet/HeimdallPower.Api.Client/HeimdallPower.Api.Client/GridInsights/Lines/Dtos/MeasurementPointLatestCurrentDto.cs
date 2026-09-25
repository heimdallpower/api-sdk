namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record MeasurementPointLatestCurrentDto
{
    /// <summary>
    /// The id of the measurement point.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid MeasurementPointId { get; init; }

    /// <summary>
    /// Time (in UTC) when the current was measured.
    /// </summary>
    /// <example>2024-07-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The latest current, in amperes, measured at this measurement point.
    /// </summary>
    /// <example>452.3</example>
    public double Value { get; init; }
}
