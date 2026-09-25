namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record MeasurementPointLatestConductorTemperatureDto
{
    /// <summary>
    /// The id of the measurement point.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid MeasurementPointId { get; init; }

    /// <summary>
    /// Time (in UTC) when the conductor temperature was measured.
    /// </summary>
    /// <example>2024-07-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The latest conductor temperature measured at this measurement point.
    /// </summary>
    /// <example>64.3</example>
    public double Value { get; init; }
}
