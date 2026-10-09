namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallSpanDlrDto
{
    /// <summary>
    /// Time (in UTC) when the Heimdall DLR was calculated for the span.
    /// </summary>
    /// <example>2024-07-01T12:00:00.001Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The Heimdall DLR value for the span at the given timestamp. The unit is given by the response's unit:
    /// amperes for current (default), MVA for apparent_power.
    /// </summary>
    /// <example>412.8</example>
    public double Value { get; init; }

    /// <summary>
    /// Indicates whether the Heimdall DLR for the span is a fallback value. Only applies to grid owners opting in for this feature.
    /// </summary>
    /// <example>false</example>
    public bool IsFallback { get; init; }
}
