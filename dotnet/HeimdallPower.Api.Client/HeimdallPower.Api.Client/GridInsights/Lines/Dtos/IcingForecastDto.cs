namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record IcingForecastDto
{
    /// <summary>
    /// The peak ice weight across all span phases and all forecast time points.
    /// </summary>
    public required MaxIcingForecastDto Max { get; init; }

    /// <summary>
    /// List of spans on the line with their icing forecast data.
    /// </summary>
    public required IReadOnlyCollection<SpanIcingForecastDto> Spans { get; init; }
}
