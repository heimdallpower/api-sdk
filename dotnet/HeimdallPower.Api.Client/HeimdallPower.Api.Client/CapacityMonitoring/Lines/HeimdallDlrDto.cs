namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallDlrDto
{
    /// <summary>
    /// Time (in UTC) when the Heimdall DLR was calculated.
    /// </summary>
    /// <example>2024-01-01T12:00:00Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The minimum calculated ampacity (in amperes) at the given timestamp.
    /// </summary>
    /// <example>375.4</example>
    public double Value { get; init; }
}
