namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record SpanPhaseIcingForecastDto
{
    /// <summary>
    /// The id of the span phase.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid SpanPhaseId { get; init; }

    /// <summary>
    /// Forecasted icing data points for this span phase. Covers 72 hours in 30-minute intervals (144 data points).
    /// </summary>
    public required IReadOnlyCollection<IcingForecastDataPointDto> Forecast { get; init; }
}
