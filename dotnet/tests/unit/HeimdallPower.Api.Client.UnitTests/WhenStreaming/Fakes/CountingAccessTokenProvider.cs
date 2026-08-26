namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming.Fakes;

/// <summary>
/// A test double for <see cref="IAccessTokenProvider"/> that tracks how many times a token
/// was acquired, so tests can assert on refresh/reuse behavior.
/// </summary>
internal sealed class CountingAccessTokenProvider(DateTimeOffset? expiresOn = null) : IAccessTokenProvider
{
    public int AcquireTokenCallCount { get; private set; }

    public Task AcquireTokenAsync(CancellationToken cancellationToken = default)
    {
        AcquireTokenCallCount++;
        return Task.CompletedTask;
    }

    public DateTimeOffset GetTokenExpiry() => expiresOn ?? DateTimeOffset.UtcNow.AddHours(1);

    public IDictionary<string, string> GetAccessHeaders() =>
        new Dictionary<string, string>
        {
            { "Authorization", $"Bearer stub-token-{AcquireTokenCallCount}" },
            { "x-region", "stub-region" },
        };
}
