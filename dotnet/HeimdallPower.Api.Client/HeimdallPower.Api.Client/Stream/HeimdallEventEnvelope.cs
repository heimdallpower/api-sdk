using System.Text.Json;

namespace HeimdallPower.Api.Client.Stream;

public record HeimdallEventEnvelope(
    string SchemaVersion,
    string Metric,
    string Unit,
    JsonElement Data)
{
    private HeimdallDlrEvent? _heimdallDlr;

    public HeimdallDlrEvent? HeimdallDlr
    {
        get
        {
            return _heimdallDlr ??= Data.Deserialize<HeimdallDlrEvent>(HeimdallStreamJsonSerializerOptions.Default);
        }
    }
}
