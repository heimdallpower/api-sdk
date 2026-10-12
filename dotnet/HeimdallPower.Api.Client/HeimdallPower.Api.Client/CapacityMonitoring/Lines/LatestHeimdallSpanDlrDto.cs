namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record LatestHeimdallSpanDlrDto
{
    /// <summary>
    /// The id of the span.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanId { get; init; }

    /// <summary>
    /// The latest Heimdall DLR for the span, calculated at the same timestamp as the line value.
    /// </summary>
    public required HeimdallSpanDlrDto HeimdallDlr { get; init; }
}
