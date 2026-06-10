using HeimdallPower.Api.Client.CapacityMonitoring.Facilities.Dtos;

namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

public record CircuitRatingResponse
{
    /// <summary>
    /// The measured quantity, mirroring the metric query parameter.
    /// </summary>
    /// <example>Current</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    public required IEnumerable<CircuitRatingDto> CircuitRatings { get; init; }
}
