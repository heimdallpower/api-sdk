using HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.Fakes;

/// <summary>
/// Creates a <see cref="HeimdallApiClient"/> wired to a fake transport and a stub token provider,
/// so the public client methods can be exercised end to end without network or authentication.
/// </summary>
internal static class HeimdallApiClientFactory
{
    public static HeimdallApiClient Create(HttpMessageHandler handler) =>
        new(new HeimdallApiHttpClient(
            new StubAccessTokenProvider(),
            new HttpClient(handler) { BaseAddress = new Uri("https://fake-api.example.com") }));
}
