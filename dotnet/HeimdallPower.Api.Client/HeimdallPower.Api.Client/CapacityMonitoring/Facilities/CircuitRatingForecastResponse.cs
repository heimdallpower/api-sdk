namespace HeimdallPower.Api.Client.CapacityMonitoring.Facilities;

public record CircuitRatingForecastResponse
{
    /// <summary>
    /// The kind of data does this response contain.
    /// </summary>
    /// <example>Circuit rating forecast</example>
    public string Metric { get; init; }

    /// <summary>
    /// The unit of measurement for the metric.
    /// </summary>
    /// <example>Ampere</example>
    public string Unit { get; init; }

    /// <summary>
    /// The timestamp when the forecasts were last updated.
    /// </summary>
    /// <example>2024-07-01T12:00:00.001Z</example>
    public DateTimeOffset UpdatedTimestamp { get; init; }

    /// <summary>
    /// The forecasts for a 1-hour interval starting from the updated_timestamp.
    /// The predicted forecasts include different percentages of confidence.
    /// </summary>
    public IReadOnlyList<CircuitRatingForecastDto> CircuitRatingForecasts { get; init; }
}
