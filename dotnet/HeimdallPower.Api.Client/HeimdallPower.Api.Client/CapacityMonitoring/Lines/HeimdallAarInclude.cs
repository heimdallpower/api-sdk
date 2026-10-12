namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

/// <summary>
/// Optional data to include in a Heimdall AAR response, in addition to the line-level value.
/// </summary>
public enum HeimdallAarInclude
{
    /// <summary>
    /// Additionally include a per-span breakdown of Heimdall AAR (as unaggregated data).
    /// Sent as <c>include=spans</c>.
    /// </summary>
    Spans,
}

internal static class HeimdallAarIncludeExtensions
{
    public static string ToQueryValue(this HeimdallAarInclude include) => include switch
    {
        HeimdallAarInclude.Spans => "spans",
        _ => throw new ArgumentOutOfRangeException(nameof(include), include, "Unsupported include value."),
    };
}
