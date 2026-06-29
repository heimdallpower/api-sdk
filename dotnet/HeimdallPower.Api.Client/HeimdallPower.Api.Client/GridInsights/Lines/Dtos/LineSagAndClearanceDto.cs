namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record LineSagAndClearanceDto
{
    /// <summary>
    /// The span phase with the maximum sag across all span phases on the line over the requested period.
    /// </summary>
    public required SpanPhaseMeasurementResult MaxSag { get; init; }

    /// <summary>
    /// The span phase with the minimum clearance across all span phases on the line over the requested period.
    /// Null if no span phase has clearance data.
    /// </summary>
    public required SpanPhaseMeasurementResult? MinClearance { get; init; }

    /// <summary>
    /// List of spans on the line with their sag and clearance data over time.
    /// Each span phase may contain multiple entries, one per timestamp within the period.
    /// </summary>
    public required IReadOnlyList<SpanSagAndClearanceDto> Spans { get; init; }

}
