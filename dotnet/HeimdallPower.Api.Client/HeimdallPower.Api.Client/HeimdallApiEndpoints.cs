namespace HeimdallPower.Api.Client;

/// <summary>
/// Endpoint/authority constants shared by every client (REST, streaming) in this SDK.
/// </summary>
internal static class HeimdallApiEndpoints
{
    public const string ApiUrl = "https://external-api.heimdallcloud.com";
    public const string StreamUrl = "https://stream-api.heimdallcloud.com";
    private const string Policy = "B2C_1A_CLIENTCREDENTIALSFLOW";
    private const string Instance = "https://hpadb2cprod.b2clogin.com";
    private const string Domain = "hpadb2cprod.onmicrosoft.com";
    public const string Scope = $"https://{Domain}/dc5758ae-4eea-416e-9e61-812914d9a49a/.default";
    public const string Authority = $"{Instance}/tfp/{Domain}/{Policy}";
}
