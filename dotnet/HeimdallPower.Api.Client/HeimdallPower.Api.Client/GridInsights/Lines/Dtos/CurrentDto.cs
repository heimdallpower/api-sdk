namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record CurrentDto
{
    /// <summary>
    /// Time (in UTC) when the current was measured.
    /// </summary>
    /// <example>2023-12-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The maximum current measured for the line at the given time.
    /// </summary>
    /// <example>500.5</example>
    public double Value { get; init; }

    /// <summary>
    /// The id of the span where the maximum current was measured.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid AtSpanId { get; init; }
}
