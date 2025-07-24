namespace HeimdallPower.Api.Client.Assets;

/// <summary>
/// A span is a segment of a line between two towers (masts), uniquely identified by the mast pair.
/// A span includes one or more span phases.
/// </summary>
public record SpanDto
{
    /// <summary>
    /// Unique identifier of the span.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid Id { get; init; }

    /// <summary>
    /// Name of the first mast in the span.
    /// </summary>
    /// <example>Mast A</example>
    public string? MastNameA { get; init; }

    /// <summary>
    /// Name of the second mast in the span
    /// </summary>
    /// <example>Mast B</example>
    public string? MastNameB { get; init; }

    /// <summary>
    /// List of span phases associated with the span.
    /// </summary>
    public IReadOnlyCollection<SpanPhaseDto> SpanPhases { get; init; }
}
