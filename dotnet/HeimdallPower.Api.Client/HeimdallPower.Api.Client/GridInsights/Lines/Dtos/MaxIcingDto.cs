namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record MaxIcingDto
{
    /// <summary>
    /// The maximum mass of ice accumulated on the conductor.
    /// </summary>
    public required SpanPhaseMeasurementResult IceWeight { get; init; }

    /// <summary>
    /// The maximum mechanical tension force in the conductor, which increases as ice accumulates.
    /// </summary>
    public required SpanPhaseMeasurementResult Tension { get; init; }

    /// <summary>
    /// Maximum safety-critical metric showing how close the conductor is to its breaking point.
    /// </summary>
    public required SpanPhaseMeasurementResult TensionPercentageOfBreakStrength { get; init; }
}
