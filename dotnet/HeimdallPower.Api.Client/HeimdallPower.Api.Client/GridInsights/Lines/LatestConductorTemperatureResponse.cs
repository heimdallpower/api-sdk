namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LatestConductorTemperatureResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Conductor temperature</example>
    public string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>C</example>
    public string Unit { get; init; }

    /// <summary>
    /// The conductor temperature measurements containing timestamp and min/max values
    /// </summary>
    public ConductorTemperatureDto ConductorTemperature { get; init; }
}
