namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

/// <summary>
/// Creates pre-wired <see cref="HeimdallApiHttpClient"/> instances for unit tests,
/// bypassing real authentication and HTTP traffic.
/// </summary>
internal static class HeimdallApiHttpClientFactory
{
    public static HeimdallApiHttpClient Create(FakeHttpMessageHandler handler) =>
        new(new StubAccessTokenProvider(),
            new HttpClient(handler) { BaseAddress = new Uri("https://fake-api.example.com") });
}

