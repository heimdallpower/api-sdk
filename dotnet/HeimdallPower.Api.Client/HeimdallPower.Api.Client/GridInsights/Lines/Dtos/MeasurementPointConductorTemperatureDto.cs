namespace HeimdallPower.Api.Client.GridInsights.Lines.Dtos;

public record MeasurementPointConductorTemperatureDto
{
    /// <summary>
    /// The id of the measurement point.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid MeasurementPointId { get; init; }

    /// <summary>
    /// Conductor temperature readings for this measurement point within the requested time range.
    /// </summary>
    public required IReadOnlyList<ConductorTemperatureDataPointDto> Temperatures { get; init; }
}
