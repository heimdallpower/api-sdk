using HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

namespace HeimdallPower.Api.Client.GridInsights.Lines;

public record IcingForecastResponse
{
    /// <summary>
    /// The kind of data this response contains.
    /// </summary>
    /// <example>Icing forecast</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of ice weight measurements. <c>kg/m</c> for metric, <c>lb/ft</c> for imperial.
    /// </summary>
    /// <example>kg/m</example>
    public required string Unit { get; init; }

    /// <summary>
    /// Icing forecast for the line organized by spans and span phases.
    /// </summary>
    public required IcingForecastDto Icing { get; init; }
}
