namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record SpanPhaseIcingDto
{
    /// <summary>
    /// The id of the span phase the measurement belongs to.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanPhaseId { get; init; }

    /// <summary>
    /// Time (UTC) when the icing measurements were calculated for the span phase. Timestamps may differ per conductor due to data availability.
    /// </summary>
    /// <example>2024-01-15T12:34:56Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The mass of ice accumulated on the conductor.
    /// </summary>
    public required MeasurementResult IceWeight { get; init; }

    /// <summary>
    /// The mechanical tension force in the conductor, which increases as ice accumulates.
    /// </summary>
    public required MeasurementResult Tension { get; init; }

    /// <summary>
    /// Safety-critical metric showing how close the conductor is to its breaking point.
    /// </summary>
    public required MeasurementResult TensionPercentageOfBreakStrength { get; init; }
}
