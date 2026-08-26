using System.Reflection;

namespace HeimdallPower.Api.Client;

/// <summary>
/// Builds the x-client-name/x-client-version (plus any caller-supplied metadata) headers sent by every SDK client.
/// </summary>
internal static class ClientHeaders
{
    private const string ClientName = "dotnet-sdk";
    private static readonly string AssemblyVersion = Assembly.GetExecutingAssembly().GetName().Version?.ToString() ?? "0.0.0";

    public static Dictionary<string, string> Build(Dictionary<string, string>? clientMetadata)
    {
        var headers = new Dictionary<string, string>
        {
            { "x-client-name", ClientName },
            { "x-client-version", AssemblyVersion },
        };

        if (clientMetadata != null)
        {
            foreach (var kvp in clientMetadata)
            {
                headers[kvp.Key] = kvp.Value; // Overwrite defaults if present
            }
        }

        return headers;
    }
}
