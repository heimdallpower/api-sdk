namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record ApparentPowerDto
{
    /// <summary>
    /// Time (in UTC) when the underlying current was measured.
    /// </summary>
    /// <example>2024-07-01T12:00:00.001Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The apparent power derived for the line at the given time, in MVA.
    /// </summary>
    /// <example>156.7</example>
    public double Value { get; init; }

    /// <summary>
    /// The id of the span where the current used to derive the apparent power was measured.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid AtSpanId { get; init; }
}
