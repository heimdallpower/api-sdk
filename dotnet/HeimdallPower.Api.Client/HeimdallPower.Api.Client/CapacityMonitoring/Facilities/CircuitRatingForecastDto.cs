namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

public record CircuitRatingForecastDto
{
    /// <summary>
    /// Timestamp for the predicted forecast.
    /// </summary>
    /// <example>2024-01-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The base prediction value for the forecast.
    /// </summary>
    public required ProbabilisticCircuitRatingDto Prediction { get; init; }

    /// <summary>
    /// The 80th percentile prediction value, representing an 80% confidence interval.
    /// </summary>
    public required ProbabilisticCircuitRatingDto P80 { get; init; }

    /// <summary>
    /// The 90th percentile prediction value, representing a 90% confidence interval.
    /// </summary>
    public required ProbabilisticCircuitRatingDto P90 { get; init; }

    /// <summary>
    /// The 95th percentile prediction value, representing a 95% confidence interval.
    /// </summary>
    public required ProbabilisticCircuitRatingDto P95 { get; init; }

    /// <summary>
    /// The 99th percentile prediction value, representing a 99% confidence interval.
    /// </summary>
    public required ProbabilisticCircuitRatingDto P99 { get; init; }
}
