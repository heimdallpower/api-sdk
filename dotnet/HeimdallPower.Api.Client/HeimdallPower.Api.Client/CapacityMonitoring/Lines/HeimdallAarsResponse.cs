namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallAarsResponse
{
    /// <summary>
    /// A human-readable label identifying the rating returned by this endpoint, independent of the quantity parameter.
    /// </summary>
    /// <example>Heimdall AAR</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response. Depends on the requested quantity:
    /// "Ampere" for current (default), "MVA" for apparent_power.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// List of Heimdall AAR values within the requested time range. May be empty if no data exists for the period.
    /// </summary>
    public required List<HeimdallAarDto> HeimdallAars { get; init; }
}
