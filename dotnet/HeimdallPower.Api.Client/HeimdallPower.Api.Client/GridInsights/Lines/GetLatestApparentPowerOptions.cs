namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetLatestApparentPowerAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetLatestApparentPowerOptions
{
    /// <summary>
    /// Optional cut-off time (UTC). If the latest apparent power is older than this value, the API returns 404 Not Found.
    /// If omitted, the API defaults to 20 minutes before the request, so a line that has not reported since then returns 404.
    /// </summary>
    public DateTimeOffset? Since { get; init; }
}
