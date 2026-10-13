namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallAarDto
{
    /// <summary>
    /// Timestamp of the Heimdall AAR measurement.
    /// </summary>
    /// <example>2023-10-25T13:45:30Z</example>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// The measured value for this timestamp.
    /// </summary>
    /// <example>450.5</example>
    public double Value { get; init; }

    /// <summary>
    /// Identifier of the span at which the lowest ampacity was calculated.
    /// </summary>
    /// <example>00000000-0000-0000-0000-000000000000</example>
    public Guid AtSpanId { get; init; }
}
