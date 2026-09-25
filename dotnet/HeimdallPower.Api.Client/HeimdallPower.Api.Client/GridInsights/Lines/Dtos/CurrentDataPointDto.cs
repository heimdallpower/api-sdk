namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record CurrentDataPointDto
{
    /// <summary>
    /// Time (in UTC) when the current was measured.
    /// </summary>
    /// <example>2024-07-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The current, in amperes, measured at this measurement point at the given timestamp.
    /// </summary>
    /// <example>452.3</example>
    public double Value { get; init; }
}
