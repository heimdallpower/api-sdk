using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LatestLineSagAndClearanceResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>SagAndClearance</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit description for the response (multiple units across measurements).
    /// </summary>
    /// <example>Multiple (see measurements)</example>
    public required string Unit { get; init; }

    /// <summary>
    /// The sag and clearance measurement.
    /// </summary>
    public required LineSagAndClearanceDto SagAndClearance { get; init; }
}
