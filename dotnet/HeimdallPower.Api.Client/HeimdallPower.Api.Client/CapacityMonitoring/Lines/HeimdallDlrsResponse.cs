namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallDlrsResponse
{
    /// <summary>
    /// A human-readable label identifying the rating returned by this endpoint, independent of the quantity parameter.
    /// </summary>
    /// <example>Heimdall DLR</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response. Depends on the requested quantity:
    /// "Ampere" for current (default), "MVA" for apparent_power.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// List of Heimdall DLR values within the requested time range. May be empty if no data exists for the period.
    /// </summary>
    public required IReadOnlyList<HeimdallDlrDto> HeimdallDlrs { get; init; }

    /// <summary>
    /// Per-span breakdown of Heimdall DLR over the requested time range. Spans without any Heimdall DLR in the period are omitted.
    /// Only present when <see cref="HeimdallDlrInclude.Spans"/> is requested; otherwise null.
    /// </summary>
    public IReadOnlyList<HeimdallSpanDlrSeriesDto>? HeimdallSpanDlrs { get; init; }
}
