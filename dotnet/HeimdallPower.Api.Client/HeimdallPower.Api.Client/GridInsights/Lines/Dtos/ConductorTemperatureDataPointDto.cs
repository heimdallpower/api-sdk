namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record ConductorTemperatureDataPointDto
{
    /// <summary>
    /// Time (in UTC) when the conductor temperature was measured.
    /// </summary>
    /// <example>2024-07-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The conductor temperature measured at this measurement point at the given timestamp.
    /// </summary>
    /// <example>64.3</example>
    public double Value { get; init; }
}
