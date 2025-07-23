namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;

public record HeimdallDlrForecastResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Heimdall DLR forecast</example>
    public string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>Ampere</example>
    public string Unit { get; init; }

    /// <summary>
    /// The timestamp when the forecasts were last updated.
    /// </summary>
    /// <example>2024-01-19T10:30:00Z</example>
    public DateTimeOffset UpdatedTimestamp { get; init; }

    /// <summary>
    /// The forecasts for a 1-hour interval starting from the updated_timestamp.
    /// The predicted forecasts include different percentages of confidence.
    /// </summary>
    public IReadOnlyCollection<ForecastDto> HeimdallDlrForecasts { get; init; }
}
