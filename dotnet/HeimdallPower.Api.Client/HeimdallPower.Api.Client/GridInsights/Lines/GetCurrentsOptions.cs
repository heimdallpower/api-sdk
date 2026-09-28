namespace HeimdallPower.Api.Client.GridInsights.Lines;

/// <summary>
/// Optional query parameters for <see cref="IHeimdallApiClient.GetCurrentsAsync"/>.
/// Unset properties fall back to the documented defaults.
/// </summary>
public sealed record GetCurrentsOptions
{
    /// <summary>
    /// Set to <see cref="CurrentInclude.MeasurementPoints"/> to additionally include a per-measurement-point breakdown of current over the requested time range, organized by span and span phase. Omitted by default.
    /// </summary>
    public CurrentInclude? Include { get; init; }
}
