namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record SpanIcingForecastDto
{
    /// <summary>
    /// The id of the span.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanId { get; init; }

    /// <summary>
    /// List of span phases (conductors) within this span with their icing forecast.
    /// </summary>
    public required IReadOnlyCollection<SpanPhaseIcingForecastDto> SpanPhases { get; init; }
}
