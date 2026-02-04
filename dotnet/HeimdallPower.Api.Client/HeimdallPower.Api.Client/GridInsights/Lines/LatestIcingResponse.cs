using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LatestIcingResponse
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
    /// The icing measurements including max and per-span/phase values.
    /// </summary>
    public required IcingDto Icing { get; init; }
}
