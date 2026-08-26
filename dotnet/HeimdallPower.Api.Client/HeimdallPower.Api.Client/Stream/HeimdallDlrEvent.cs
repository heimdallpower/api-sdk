namespace HeimdallPower.Api.Client.Stream;

public record HeimdallDlrEvent(
    Guid AtLineId,
    Guid AtSpanId,
    DateTimeOffset Timestamp,
    double Value,
    bool IsFallback)
{
    public const string MetricName = "Heimdall DLR";
}
