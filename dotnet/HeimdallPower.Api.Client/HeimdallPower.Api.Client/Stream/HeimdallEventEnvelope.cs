using HeimdallPower.Api.Client.Stream.CapacityMonitoring.Lines;
using System.Text.Json;

namespace HeimdallPower.Api.Client.Stream;

/// <summary>
/// A single event received from the Heimdall Stream API.
/// </summary>
/// <param name="SchemaVersion">The version of the envelope schema.</param>
/// <param name="Metric">The kind of event carried in <paramref name="Data"/>, e.g. <see cref="HeimdallDlrEvent.EventName"/>.</param>
/// <param name="Unit">The unit of the value carried in <paramref name="Data"/>.</param>
/// <param name="Data">The raw, metric-specific event payload. Use <see cref="HeimdallDlr"/> to access it as a typed <see cref="HeimdallDlrEvent"/>.</param>
public record HeimdallEventEnvelope(
    string SchemaVersion,
    string Metric,
    string Unit,
    JsonElement Data)
{
    private HeimdallDlrEvent? _heimdallDlr;

    /// <summary>
    /// <see cref="Data"/> deserialized as a <see cref="HeimdallDlrEvent"/>, or <see langword="null"/> if it cannot be deserialized as one.
    /// Only meaningful when <see cref="Metric"/> equals "Heimdall DLR" />.
    /// </summary>
    public HeimdallDlrEvent? HeimdallDlr
    {
        get
        {
            return _heimdallDlr ??= Data.Deserialize<HeimdallDlrEvent>(HeimdallStreamJsonSerializerOptions.Default);
        }
    }
}
