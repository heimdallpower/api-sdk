namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallSpanDlrSeriesDto
{
    /// <summary>
    /// The id of the span.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanId { get; init; }

    /// <summary>
    /// Heimdall DLR values for this span within the requested time range, ordered by timestamp.
    /// </summary>
    public required IReadOnlyList<HeimdallSpanDlrDto> HeimdallDlrs { get; init; }
}
