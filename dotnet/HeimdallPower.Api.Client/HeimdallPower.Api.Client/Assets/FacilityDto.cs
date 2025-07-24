namespace HeimdallPower.Api.Client.Assets;

/// <summary>
/// A facility is a collection of components that allows grid owners to define limiting components and configurations for a power line.
/// Among the components that a facility can have is a line.
/// A facility can have zero or one line.
/// </summary>
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
