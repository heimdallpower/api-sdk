namespace HeimdallPower.Api.Client.Assets;

/// <summary>
/// A grid owner represents the organization that owns the assets.
/// A grid owner includes one or more facilities.
/// </summary>
public record GridOwnerDto
{
    /// <summary>
    /// Name of the grid owner.
    /// </summary>
    /// <example>Grid Owner A</example>
    public required string Name { get; init; }

    /// <summary>
    /// List of facilities associated with the grid owner.
    /// </summary>
    /// <example>Facility A</example>
    public required IReadOnlyCollection<FacilityDto> Facilities { get; init; }
}
