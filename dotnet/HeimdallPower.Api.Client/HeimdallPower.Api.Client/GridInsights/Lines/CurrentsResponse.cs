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
}
