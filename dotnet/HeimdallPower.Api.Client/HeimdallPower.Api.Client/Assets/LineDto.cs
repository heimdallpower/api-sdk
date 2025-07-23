namespace HeimdallPower.Api.Client.Assets;

public record LineDto
{
    /// <summary>
    /// Unique identifier of the line.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid Id { get; init; }

    /// <summary>
    /// Name of the line.
    /// </summary>
    /// <example>Line A</example>
    public string Name { get; init; }

    /// <summary>
    /// The available forecast length in hours, used as a query parameter for DLR forecasts.
    /// The maximum is 240 hours.
    /// </summary>
    /// <example>72</example>
    public int AvailableForecastHours { get; init; }

    /// <summary>
    /// List of spans belonging to the line.
    /// </summary>
    public IReadOnlyCollection<SpanDto> Spans { get; init; }
}
