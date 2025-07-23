namespace HeimdallPower.Api.Client.Assets;

public record GridOwnerDto
{
    /// <summary>
    /// Name of the grid owner.
    /// </summary>
    /// <example>Grid Owner A</example>
    public string Name { get; init; }

    /// <summary>
    /// List of facilities associated with the grid owner.
    /// </summary>
    /// <example>Facility A</example>
    public IReadOnlyCollection<FacilityDto> Facilities { get; init; }
}
