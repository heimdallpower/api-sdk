namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

public record ForecastDto
{
    /// <summary>
    /// Timestamp for the predicted forecast.
    /// </summary>
    /// <example>2024-01-01T12:00:00Z</example>
    public DateTime Timestamp { get; init; }

    /// <summary>
    /// The base prediction value for the forecast.
    /// </summary>
    public ProbabilisticLineAmpacityDto Prediction { get; init; }

    /// <summary>
    /// The 80th percentile prediction value, representing an 80% confidence interval.
    /// </summary>
    public ProbabilisticLineAmpacityDto P80 { get; init; }

    /// <summary>
    /// The 90th percentile prediction value, representing a 90% confidence interval.
    /// </summary>
    public ProbabilisticLineAmpacityDto P90 { get; init; }

    /// <summary>
    /// The 95th percentile prediction value, representing a 95% confidence interval.
    /// </summary>
    public ProbabilisticLineAmpacityDto P95 { get; init; }

    /// <summary>
    /// The 99th percentile prediction value, representing a 99% confidence interval.
    /// </summary>
    public ProbabilisticLineAmpacityDto P99 { get; init; }
}
