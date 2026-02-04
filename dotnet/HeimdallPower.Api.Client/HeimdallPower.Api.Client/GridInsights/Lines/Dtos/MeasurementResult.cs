namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record MeasurementResult()
{
    /// <summary>
    /// The numerical value of the measurement.
    /// </summary>
    public double Value { get; init; }

    /// <summary>
    /// The unit of the measurement.
    /// </summary>
    public required string Unit { get; init; }
}
