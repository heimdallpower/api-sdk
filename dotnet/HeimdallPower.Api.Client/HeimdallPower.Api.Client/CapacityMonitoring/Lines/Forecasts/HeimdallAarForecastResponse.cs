namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

public record HeimdallAarForecastResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Heimdall AAR forecast</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// Timestamp when the forecast was last updated.
    /// </summary>
    /// <example>2024-01-15T13:45:30Z</example>
    public DateTimeOffset UpdatedTimestamp { get; init; }

    /// <summary>
    /// The forecasts for a 1-hour interval starting from the updated_timestamp.
    /// The predicted forecasts include different percentages of confidence.
    /// </summary>
    public required IReadOnlyCollection<ForecastDto> HeimdallAarForecasts { get; init; }
}
