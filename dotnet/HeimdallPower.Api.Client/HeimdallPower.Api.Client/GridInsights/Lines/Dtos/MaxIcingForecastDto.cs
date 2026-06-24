namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record MaxIcingForecastDto
{
    /// <summary>
    /// The peak ice weight across all span phases and all forecast time points.
    /// </summary>
    public required SpanPhaseMeasurementResult IceWeight { get; init; }
}
