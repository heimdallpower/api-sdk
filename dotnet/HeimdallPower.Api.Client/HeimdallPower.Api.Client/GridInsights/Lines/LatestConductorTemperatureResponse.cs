using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LatestConductorTemperatureResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Conductor temperature</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>C</example>
    public required string Unit { get; init; }

    /// <summary>
    /// The conductor temperature measurements containing timestamp and min/max values
    /// </summary>
    public required ConductorTemperatureDto ConductorTemperature { get; init; }

    /// <summary>
    /// Per-measurement-point breakdown of the latest conductor temperature, organized by span and span phase.
    /// Only present when <c>include</c> is set to "measurement_points" in the request; otherwise null.
    /// </summary>
    public IReadOnlyList<SpanLatestConductorTemperatureDto>? MeasurementPointTemperatures { get; init; }
}
