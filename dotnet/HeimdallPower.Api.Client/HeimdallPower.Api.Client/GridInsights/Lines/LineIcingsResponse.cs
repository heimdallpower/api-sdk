using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LineIcingsResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Icing</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit description for the response (multiple units across measurements).
    /// </summary>
    /// <example>Multiple (see measurements)</example>
    public required string Unit { get; init; }

    /// <summary>
    /// Icing measurements for the line over the requested time range, including the
    /// line-level maximum values and detailed measurements organized by spans and span phases.
    /// Each span phase may contain multiple entries, one per timestamp within the period.
    /// </summary>
    public required IcingDto Icing { get; init; }
}
