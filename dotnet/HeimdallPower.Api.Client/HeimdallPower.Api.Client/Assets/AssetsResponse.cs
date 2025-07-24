namespace HeimdallPower.Api.Client.Assets;

public record AssetsResponse
{
    /// <summary>
    /// List of grid owners the API consumer has access to.
    /// </summary>
    public required IReadOnlyCollection<GridOwnerDto> GridOwners { get; init; }
}
