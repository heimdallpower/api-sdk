namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record SpanPhaseMeasurementResult
{
    /// <summary>
    /// Time (UTC) when the icing measurements were calculated for the span phase. Timestamps may differ per conductor due to data availability.
    /// </summary>
    /// <example>2024-01-15T12:34:56Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The id of the span phase the measurement belongs to.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanPhaseId { get; init; }

    /// <summary>
    /// The numerical value of the measurement.
    /// </summary>
    public double Value { get; init; }

    /// <summary>
    /// The unit of the measurement value.
    /// </summary>
    public required string Unit { get; init; }
}
