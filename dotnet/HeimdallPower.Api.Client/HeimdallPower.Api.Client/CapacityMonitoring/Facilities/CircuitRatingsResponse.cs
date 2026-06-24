namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

public record CircuitRatingsResponse
{
    /// <summary>
    /// A human-readable label identifying the rating returned by this endpoint, independent of the quantity parameter.
    /// </summary>
    /// <example>Circuit rating</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response. Depends on the requested quantity:
    /// "Ampere" for current (default), "MVA" for apparent_power.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// List of circuit ratings within the requested time range.
    /// </summary>
    public required List<CircuitRatingDto> CircuitRatings { get; init; }
}
