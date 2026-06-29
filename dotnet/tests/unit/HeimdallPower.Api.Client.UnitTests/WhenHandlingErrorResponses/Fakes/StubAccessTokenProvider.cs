namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

/// <summary>
/// A test double for <see cref="IAccessTokenProvider"/> that always returns a
/// pre-baked, non-expired token so tests never hit a real auth endpoint.
/// </summary>
internal sealed class StubAccessTokenProvider : IAccessTokenProvider
{
    public Task AcquireTokenAsync() => Task.CompletedTask;

    public DateTimeOffset GetTokenExpiry() => DateTimeOffset.UtcNow.AddHours(1);

    public IDictionary<string, string> GetAccessHeaders() =>
        new Dictionary<string, string>
        {
            { "Authorization", "Bearer stub-token" },
            { "x-region", "stub-region" },
        };
}

