namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record LatestHeimdallAarResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>current</example>
    public string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public string Unit { get; init; }

    /// <summary>
    /// The latest Heimdall ambient-adjusted rating value and timestamp.
    /// </summary>
    public HeimdallAarDto HeimdallAar { get; init; }
}
