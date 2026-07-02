namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingTransientErrors.Fakes;

/// <summary>
/// A no-op token provider — tests only exercise the HTTP retry layer,
/// so the token is pre-set and never expired.
/// </summary>
internal sealed class StubAccessTokenProvider : IAccessTokenProvider
{
    public Task AcquireTokenAsync(CancellationToken cancellationToken = default) => Task.CompletedTask;

    public DateTimeOffset GetTokenExpiry()
        => DateTimeOffset.UtcNow.AddHours(1); // always valid

    public IDictionary<string, string> GetAccessHeaders()
        => new Dictionary<string, string>
        {
            { "Authorization", "Bearer stub-token" }
        };
}

