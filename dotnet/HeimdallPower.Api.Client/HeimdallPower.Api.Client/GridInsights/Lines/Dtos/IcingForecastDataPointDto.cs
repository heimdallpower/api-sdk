namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record IcingForecastDataPointDto
{
    /// <summary>
    /// Time (UTC) for this forecast data point.
    /// </summary>
    /// <example>2024-01-15T08:33:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The forecasted ice weight at this time point.
    /// </summary>
    public required MeasurementResult IceWeight { get; init; }
}
