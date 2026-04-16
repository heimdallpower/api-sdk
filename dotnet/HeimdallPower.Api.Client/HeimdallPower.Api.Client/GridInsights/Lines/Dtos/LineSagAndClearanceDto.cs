namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record LineSagAndClearanceDto
{
    /// <summary>
    /// Highest sag measurement across all spans on the line with timestamp and value.
    /// </summary>
    public required SpanPhaseMeasurementResult MaxSag { get; init; }

    /// <summary>
    /// Lowest clearance measurement across all spans on the line with timestamp and value.
    /// Null if clearance is not available.
    /// </summary>
    public required SpanPhaseMeasurementResult? MinClearance { get; init; }

    /// <summary>
    /// List of spans on the line with their sag and clearance data.
    /// </summary>
    public required IReadOnlyList<SpanSagAndClearanceDto> Spans { get; init; }

}
