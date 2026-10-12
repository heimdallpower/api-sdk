namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record LatestHeimdallSpanAarDto
{
    /// <summary>
    /// The id of the span.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanId { get; init; }

    /// <summary>
    /// The latest Heimdall AAR for the span, calculated at the same timestamp as the line value.
    /// </summary>
    public required HeimdallSpanAarDto HeimdallAar { get; init; }
}
