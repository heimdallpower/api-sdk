namespace HeimdallPower.Api.Client.Assets;

public record SpanPhaseDto
{
    /// <summary>
    /// Unique identifier of the span phase.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid Id { get; init; }

    /// <summary>
    /// Name of the span phase.
    /// </summary>
    /// <example>Phase A</example>
    public string? Name { get; init; }
}
