using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record CurrentsResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Current</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// List of current measurements within the requested time range. May be empty if no data exists for the period.
    /// </summary>
    public required IReadOnlyCollection<CurrentDto> Currents { get; init; }

    /// <summary>
    /// Per-measurement-point breakdown of current over the requested time range, organized by span and span phase.
    /// Only present when <see cref="CurrentInclude.MeasurementPoints"/> is requested; otherwise null.
    /// </summary>
    public IReadOnlyList<SpanCurrentDto>? MeasurementPointCurrents { get; init; }
}
