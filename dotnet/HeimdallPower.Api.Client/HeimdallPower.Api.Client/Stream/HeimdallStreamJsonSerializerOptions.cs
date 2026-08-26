using System.Text.Json;
using System.Text.Json.Serialization;

namespace HeimdallPower.Api.Client.Stream;

internal static class HeimdallStreamJsonSerializerOptions
{
    private static JsonSerializerOptions? _jsonOptions;

    private static JsonSerializerOptions CreateJsonOptions()
    {
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true,
            PropertyNamingPolicy = JsonNamingPolicy.SnakeCaseLower
        };
        options.Converters.Add(new JsonStringEnumConverter());
        return options;
    }

    public static JsonSerializerOptions Default
    {
        get
        {
            return _jsonOptions ??= CreateJsonOptions();
        }
    }
}
