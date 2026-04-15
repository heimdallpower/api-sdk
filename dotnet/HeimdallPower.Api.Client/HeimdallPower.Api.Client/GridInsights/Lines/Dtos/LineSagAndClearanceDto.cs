namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record LineSagAndClearanceDto
{
    /// <summary>
    /// List of spans on the line with their sag and clearance data.
    /// </summary>
    public required IReadOnlyList<SpanSagAndClearanceDto> Spans { get; init; }
}
