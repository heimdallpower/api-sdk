using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record LineSagAndClearancesResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>SagAndClearance</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response (multiple units across measurements).
    /// </summary>
    /// <example>Multiple (see measurements)</example>
    public required string Unit { get; init; }

    /// <summary>
    /// Sag and clearance measurements for the line over the requested time range,
    /// including the line-level maximum sag and minimum clearance values,
    /// as well as detailed measurements organized by spans and span phases.
    /// </summary>
    public required LineSagAndClearanceDto SagAndClearance { get; init; }
}
