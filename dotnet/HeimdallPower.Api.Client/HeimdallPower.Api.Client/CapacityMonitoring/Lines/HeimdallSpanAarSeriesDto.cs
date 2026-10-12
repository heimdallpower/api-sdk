namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallSpanAarSeriesDto
{
    /// <summary>
    /// The id of the span.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanId { get; init; }

    /// <summary>
    /// Heimdall AAR values for this span within the requested time range, ordered by timestamp.
    /// </summary>
    public required IReadOnlyList<HeimdallSpanAarDto> HeimdallAars { get; init; }
}
