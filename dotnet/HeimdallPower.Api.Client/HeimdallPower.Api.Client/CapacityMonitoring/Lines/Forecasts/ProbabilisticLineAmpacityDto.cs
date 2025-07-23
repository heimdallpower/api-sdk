namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

public record ProbabilisticLineAmpacityDto
{
    /// <summary>
    /// The ampacity value (in amperes) for the line.
    /// </summary>
    /// <example>375.4</example>
    public double Value { get; init; }

    /// <summary>
    /// Identifier of the span at which this ampacity forecast was calculated.
    /// The forecast is computed per span and timestamp, and the final dimensioning value is determined by selecting the span with the lowest ampacity.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid? AtSpanId { get; init; }
}
