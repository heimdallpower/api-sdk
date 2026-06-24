namespace HeimdallPower.Api.Client.CapacityMonitoring;

/// <summary>
/// Controls which physical quantity is returned by a rating endpoint.
/// </summary>
public enum Quantity
{
    /// <summary>
    /// Values in amperes (default).
    /// </summary>
    Current,

    /// <summary>
    /// Values converted to three-phase apparent power in MVA using S = sqrt(3) * V * I / 1,000,000.
    /// The line's operational voltage is used when set and positive; otherwise the nominal voltage is used.
    /// </summary>
    ApparentPower,
}

internal static class QuantityExtensions
{
    public static string ToQueryValue(this Quantity quantity) => quantity switch
    {
        Quantity.ApparentPower => "apparent_power",
        _ => "current",
    };
}
