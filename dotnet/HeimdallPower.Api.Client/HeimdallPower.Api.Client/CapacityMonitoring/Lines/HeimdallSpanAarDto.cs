namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallSpanAarDto
{
    /// <summary>
    /// Time (in UTC) when the Heimdall AAR was calculated for the span.
    /// </summary>
    /// <example>2024-07-01T12:00:00.001Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The Heimdall AAR value for the span at the given timestamp. The unit is given by the response's unit:
    /// amperes for current (default), MVA for apparent_power.
    /// </summary>
    /// <example>412.8</example>
    public double Value { get; init; }
}
