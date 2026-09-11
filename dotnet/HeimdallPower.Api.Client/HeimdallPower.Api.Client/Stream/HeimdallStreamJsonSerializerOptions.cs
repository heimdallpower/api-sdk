using System.Text.Json;
using System.Text.Json.Serialization;

namespace HeimdallPower.Api.Client.Stream;

/// <summary>
/// Shared, lazily-created <see cref="JsonSerializerOptions"/> used to (de)serialize Stream API payloads
/// (snake_case property names, case-insensitive matching, string enums).
/// </summary>
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

    /// <summary>
    /// The shared <see cref="JsonSerializerOptions"/> instance, created on first access.
    /// </summary>
    public static JsonSerializerOptions Default
    {
        get
        {
            return _jsonOptions ??= CreateJsonOptions();
        }
    }
}
