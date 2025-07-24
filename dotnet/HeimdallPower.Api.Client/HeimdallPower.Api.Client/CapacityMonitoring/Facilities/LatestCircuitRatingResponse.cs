namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

public record LatestCircuitRatingResponse
{
    /// <summary>
    /// The kind of data does this response contain.
    /// </summary>
    /// <example>Circuit rating</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// The circuit rating measurement with timestamp and value.
    /// </summary>
    public required CircuitRatingDto CircuitRating { get; init; }
}
