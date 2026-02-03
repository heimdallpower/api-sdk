namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record IcingDto
{
    /// <summary>
    /// The maximum icing data, i.e. max ice weight, max tension and max percentage of tensions, across all span phases on the line.
    /// </summary>
    public required MaxIcingDto Max { get; init; }

    /// <summary>
    /// List of spans on the line with their icing data.
    /// </summary>
    public required IReadOnlyCollection<SpanIcingDto> Spans { get; init; }
}
