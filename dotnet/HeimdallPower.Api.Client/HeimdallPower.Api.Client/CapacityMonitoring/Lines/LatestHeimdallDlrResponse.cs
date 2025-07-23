namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record LatestHeimdallDlrResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Heimdall DLR</example>
    public string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public string Unit { get; init; }

    /// <summary>
    /// The latest Heimdall DLR value and timestamp.
    /// </summary>
    public HeimdallDlrDto HeimdallDlr { get; init; }
}
