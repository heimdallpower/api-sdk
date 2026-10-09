namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

/// <summary>
/// Optional data to include in a Heimdall DLR response, in addition to the line-level value.
/// </summary>
public enum HeimdallDlrInclude
{
    /// <summary>
    /// Additionally include a per-span breakdown of Heimdall DLR (as unaggregated data).
    /// Sent as <c>include=spans</c>.
    /// </summary>
    Spans,
}

internal static class HeimdallDlrIncludeExtensions
{
    public static string ToQueryValue(this HeimdallDlrInclude include) => include switch
    {
        HeimdallDlrInclude.Spans => "spans",
        _ => throw new ArgumentOutOfRangeException(nameof(include), include, "Unsupported include value."),
    };
}
