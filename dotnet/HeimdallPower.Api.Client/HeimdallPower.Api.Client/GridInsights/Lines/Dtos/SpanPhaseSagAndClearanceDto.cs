namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record SpanPhaseSagAndClearanceDto
{
    /// <summary>
    /// The id of the span phase the measurement belongs to.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanPhaseId { get; init; }

    /// <summary>
    /// Time (UTC) when the measurements were calculated for the span phase. Timestamps may differ per conductor due to data availability.
    /// </summary>
    /// <example>2024-01-15T12:34:56Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The maximum vertical deflection of the conductor from the straight line between its two support points.
    /// </summary>
    public required MeasurementResult Sag { get; init; }

    /// <summary>
    /// The vertical distance between the conductor and the ground or objects below.
    /// </summary>
    public MeasurementResult? Clearance { get; init; }
}
