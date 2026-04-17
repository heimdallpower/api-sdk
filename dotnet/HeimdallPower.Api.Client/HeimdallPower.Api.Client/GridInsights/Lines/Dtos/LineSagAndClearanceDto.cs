namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record LineSagAndClearanceDto
{
    /// <summary>
    /// The span phase with the maximum sag across all span phases on the line.
    /// </summary>
    public required SpanPhaseMeasurementResult MaxSag { get; init; }

    /// <summary>
    /// The span phase with the minimum clearance across all span phases on the line.
    /// Null if no span phase has clearance data.
    /// </summary>
    public required SpanPhaseMeasurementResult? MinClearance { get; init; }

    /// <summary>
    /// Sag and clearance data grouped by span, with each span listing its span phases and their latest measurements.
    /// </summary>
    public required IReadOnlyList<SpanSagAndClearanceDto> Spans { get; init; }

}
