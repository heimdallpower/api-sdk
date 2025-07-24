namespace HeimdallPower.Api.Client.Assets;

public record FacilityDto
{
    /// <summary>
    /// Unique identifier of the facility.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid Id { get; init; }

    /// <summary>
    /// Name of the facility.
    /// </summary>
    /// <example>Facility A</example>
    public required string Name { get; init; }

    /// <summary>
    /// Line associated with the facility, if available.
    /// </summary>
    public LineDto? Line { get; init; }
}
