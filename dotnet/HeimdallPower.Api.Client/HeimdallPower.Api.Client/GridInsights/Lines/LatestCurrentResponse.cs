namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LatestCurrentResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Current</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// The latest current measurement data including timestamp and value.
    /// </summary>
    public required CurrentDto Current { get; init; }
}
