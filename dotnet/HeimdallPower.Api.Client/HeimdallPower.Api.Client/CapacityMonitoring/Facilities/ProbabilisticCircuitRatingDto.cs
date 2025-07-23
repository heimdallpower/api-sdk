namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

public record ProbabilisticCircuitRatingDto
{
    /// <summary>
    /// The ampacity value (in amperes) for the line.
    /// </summary>
    /// <example>375.4</example>
    public double Value { get; init; }

    /// <summary>
    /// Identifier of the facility component at which this ampacity forecast was calculated.
    /// The forecast is computed per facility component and timestamp, and the final dimensioning value is determined by selecting the facility component with the lowest ampacity.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid? AtFacilityComponentId { get; init; }
}
