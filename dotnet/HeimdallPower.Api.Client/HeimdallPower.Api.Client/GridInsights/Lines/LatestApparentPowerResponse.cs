using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LatestApparentPowerResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Apparent power</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the value in the response.
    /// </summary>
    /// <example>MVA</example>
    public required string Unit { get; init; }

    /// <summary>
    /// The most recent apparent power measurement for the line.
    /// </summary>
    public required ApparentPowerDto ApparentPower { get; init; }
}
