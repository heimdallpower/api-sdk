namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record HeimdallAarDto
{
    /// <summary>
    /// Timestamp of the Heimdall AAR measurement.
    /// </summary>
    /// <example>2023-10-25T13:45:30Z</example>
    public DateTime Timestamp { get; init; }

    /// <summary>
    /// The measured value for this timestamp.
    /// </summary>
    /// <example>450.5</example>
    public double Value { get; init; }
}
