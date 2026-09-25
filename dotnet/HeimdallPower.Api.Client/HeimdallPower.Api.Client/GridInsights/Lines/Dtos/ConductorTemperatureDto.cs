namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record ConductorTemperatureDto
{
    /// <summary>
    /// Time (in UTC) when the conductor temperature was measured.
    /// </summary>
    /// <example>2024-01-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The maximum conductor temperature measured for the line at the given timestamp.
    /// </summary>
    /// <example>68.7</example>
    public double Max { get; init; }

    /// <summary>
    /// The minimum conductor temperature measured for the line at the given timestamp.
    /// </summary>
    /// <example>55.2</example>
    public double? Min { get; init; }

    /// <summary>
    /// The id of the span where the maximum conductor temperature was measured.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid MaxAtSpanId { get; init; }

    /// <summary>
    /// The id of the span where the minimum conductor temperature was measured. Null when no minimum is available.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid? MinAtSpanId { get; init; }
}
