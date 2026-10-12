namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record LatestHeimdallAarResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>current</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// The latest Heimdall ambient-adjusted rating value and timestamp.
    /// </summary>
    public required HeimdallAarDto HeimdallAar { get; init; }

    /// <summary>
    /// Per-span breakdown of the latest Heimdall AAR, calculated at the same timestamp as <see cref="HeimdallAar"/>.
    /// Spans without a Heimdall AAR at that timestamp are omitted.
    /// Only present when <see cref="HeimdallAarInclude.Spans"/> is requested; otherwise null.
    /// </summary>
    public IReadOnlyList<LatestHeimdallSpanAarDto>? HeimdallSpanAars { get; init; }
}
