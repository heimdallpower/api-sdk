namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record CurrentDto
{
    /// <summary>
    /// Time (in UTC) when the current was measured.
    /// </summary>
    /// <example>2023-12-01T12:00:00Z</example>
    public DateTime Timestamp { get; init; }

    /// <summary>
    /// The maximum current measured for the line at the given time.
    /// </summary>
    /// <example>500.5</example>
    public double Value { get; init; }
}
