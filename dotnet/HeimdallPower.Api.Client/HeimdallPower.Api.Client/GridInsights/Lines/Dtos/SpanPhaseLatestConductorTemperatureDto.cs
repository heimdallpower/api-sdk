namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record SpanPhaseLatestConductorTemperatureDto
{
    /// <summary>
    /// The id of the span phase.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanPhaseId { get; init; }

    /// <summary>
    /// Measurement points (one per sub-conductor) within this span phase.
    /// </summary>
    public required IReadOnlyList<MeasurementPointLatestConductorTemperatureDto> MeasurementPoints { get; init; }
}
