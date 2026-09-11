namespace HeimdallPower.Api.Client.Stream.CapacityMonitoring.Lines;

/// <summary>
/// A Heimdall Dynamic Line Rating (DLR) reading for a span, as carried in <see cref="HeimdallEventEnvelope.Data"/>
/// when <see cref="HeimdallEventEnvelope.Metric"/> equals <see cref="EventName"/>.
/// </summary>
/// <param name="AtLineId">The ID of the line the span belongs to.</param>
/// <param name="AtSpanId">The ID of the span the reading applies to.</param>
/// <param name="Timestamp">Time (in UTC) when the Heimdall DLR was calculated. <example>2024-01-01T12:00:00Z</example></param>
/// <param name="Value">The minimum calculated ampacity, in the unit specified by <see cref="HeimdallEventEnvelope.Unit"/>. <example>375.4</example></param>
/// <param name="IsFallback">Indicates whether the Heimdall DLR is a fallback value. Only applies to grid owners opting in for this feature.</param>
public record HeimdallDlrEvent(
    Guid AtLineId,
    Guid AtSpanId,
    DateTimeOffset Timestamp,
    double Value,
    bool IsFallback)
{
    /// <summary>
    /// The value of SSE 'event:' field for Heimdall DLR events.
    /// </summary>
    public const string EventName = "heimdall_dlr";
}
