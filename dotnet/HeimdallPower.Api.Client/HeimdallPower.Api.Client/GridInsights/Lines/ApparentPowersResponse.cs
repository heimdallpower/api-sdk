using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record ApparentPowersResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Apparent power</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response.
    /// </summary>
    /// <example>MVA</example>
    public required string Unit { get; init; }

    /// <summary>
    /// List of apparent power values within the requested time range. May be empty if no data exists for the period.
    /// </summary>
    public required IReadOnlyCollection<ApparentPowerDto> ApparentPowers { get; init; }
}
