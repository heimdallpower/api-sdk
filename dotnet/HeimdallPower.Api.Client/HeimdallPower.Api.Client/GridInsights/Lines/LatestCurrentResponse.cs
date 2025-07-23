namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LatestCurrentResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Current</example>
    public string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public string Unit { get; init; }

    /// <summary>
    /// The latest current measurement data including timestamp and value.
    /// </summary>
    public CurrentDto Current { get; init; }
}
