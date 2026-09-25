using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record ConductorTemperaturesResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Conductor temperature</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response.
    /// </summary>
    /// <example>C</example>
    public required string Unit { get; init; }

    /// <summary>
    /// List of conductor temperature measurements within the requested time range. May be empty if no data exists for the period.
    /// </summary>
    public required IReadOnlyCollection<ConductorTemperatureDto> ConductorTemperatures { get; init; }

    /// <summary>
    /// Per-measurement-point breakdown of conductor temperature over the requested time range, organized by span and span phase.
    /// Only present when <c>include</c> is set to "measurement_points" in the request; otherwise null.
    /// </summary>
    public IReadOnlyList<SpanConductorTemperatureDto>? MeasurementPointTemperatures { get; init; }
}
