namespace HeimdallPower.Api.Client.Stream.CapacityMonitoring.Lines;

/// <summary>
/// A Heimdall Dynamic Line Rating (DLR) reading for a span, as carried in <see cref="HeimdallEventEnvelope.Data"/>
/// when <see cref="HeimdallEventEnvelope.Metric"/> equals <see cref="MetricName"/>.
/// </summary>
/// <param name="AtLineId">The ID of the line the span belongs to.</param>
/// <param name="AtSpanId">The ID of the span the reading applies to.</param>
/// <param name="Timestamp">The time the reading was taken.</param>
/// <param name="Value">The DLR value, in the unit specified by <see cref="HeimdallEventEnvelope.Unit"/>.</param>
/// <param name="IsFallback">Whether this is a fallback rating, used when a live DLR value is unavailable.</param>
public record HeimdallDlrEvent(
    Guid AtLineId,
    Guid AtSpanId,
    DateTimeOffset Timestamp,
    double Value,
    bool IsFallback)
{
    /// <summary>
    /// The value of <see cref="HeimdallEventEnvelope.Metric"/> for Heimdall DLR events.
    /// </summary>
    public const string MetricName = "Heimdall DLR";
}
