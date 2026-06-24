using System.Net;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingTransientErrors.Fakes;

internal static class HeimdallApiHttpClientFactory
{
    /// <summary>
    /// Creates a <see cref="HeimdallApiHttpClient"/> backed by <paramref name="handler"/>.
    /// The delay function is a no-op so tests complete instantly.
    /// </summary>
    public static HeimdallApiHttpClient Create(FakeHttpMessageHandler handler)
    {
        var httpClient = new HttpClient(handler) { BaseAddress = new Uri("https://fake.heimdallcloud.com") };
        return new HeimdallApiHttpClient(
            accessTokenProvider: new StubAccessTokenProvider(),
            httpClient: httpClient,
            clientMetadata: null,
            delayFunc: _ => Task.CompletedTask); // no real sleeping in unit tests
    }

    /// <summary>Convenience: single repeating response.</summary>
    public static HeimdallApiHttpClient CreateWithFixedResponse(HttpResponseMessage response)
        => Create(new FakeHttpMessageHandler(response));

    /// <summary>Convenience: a sequence of responses (e.g. N failures then a success).</summary>
    public static HeimdallApiHttpClient CreateWithSequence(params HttpResponseMessage[] responses)
        => Create(new FakeHttpMessageHandler(responses));
}

