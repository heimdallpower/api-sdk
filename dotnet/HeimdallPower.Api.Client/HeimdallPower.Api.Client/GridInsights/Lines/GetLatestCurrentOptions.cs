namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetLatestCurrentAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetLatestCurrentOptions
{
    /// <summary>
    /// Optional cut-off time (UTC). If the latest current is older than this value, the API returns 404 Not Found.
    /// </summary>
    public DateTimeOffset? Since { get; init; }

    /// <summary>
    /// Set to <see cref="CurrentInclude.MeasurementPoints"/> to additionally include a per-measurement-point breakdown of the latest current, organized by span and span phase. Omitted by default.
    /// </summary>
    public CurrentInclude? Include { get; init; }
}
