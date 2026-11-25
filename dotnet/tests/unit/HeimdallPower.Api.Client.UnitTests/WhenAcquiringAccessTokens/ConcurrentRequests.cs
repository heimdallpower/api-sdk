using System.Net;
using System.Text;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenAcquiringAccessTokens;

/// <summary>
/// Verifies that concurrent requests acquire an access token one at a time: a request that waits for
/// another's acquisition reuses its token, and one that waits too long fails with <see cref="TimeoutException"/>
/// instead of acquiring a token alongside it.
/// </summary>
[Trait("Category", "Unit")]
public class ConcurrentRequests
{
    private const string EmptyAssetsJson = """{"data":{"grid_owners":[]}}""";

    private readonly CountingHttpMessageHandler _api = new(_ =>
        new HttpResponseMessage(HttpStatusCode.OK) { Content = new StringContent(EmptyAssetsJson, Encoding.UTF8, "application/json") });

    private readonly BlockingAccessTokenProvider _tokens = new();

    private HeimdallApiClient CreateClient(TimeSpan tokenLockTimeout) =>
        new(new HeimdallApiHttpClient(
            _tokens,
            new HttpClient(_api) { BaseAddress = new Uri("https://fake-api.example.com") },
            tokenLockTimeout: tokenLockTimeout));

    [Fact]
    public async Task ShouldReuseToken_WhenWaitingForAnotherRequestsAcquisition()
    {
        var client = CreateClient(TimeSpan.FromSeconds(30));
        var first = client.GetAssetsAsync();
        await _tokens.FirstAcquisitionStarted;
        var second = client.GetAssetsAsync();

        _tokens.CompleteFirstAcquisition();
        await Task.WhenAll(first, second).WaitAsync(TimeSpan.FromSeconds(10));

        Assert.Equal(1, _tokens.AcquisitionCount);
        Assert.Equal(2, _api.CallCount);
    }

    [Fact]
    public async Task ShouldThrowTimeout_WhenAnotherRequestsAcquisitionTakesTooLong()
    {
        var client = CreateClient(TimeSpan.FromMilliseconds(100));
        var first = client.GetAssetsAsync();
        await _tokens.FirstAcquisitionStarted;

        await Assert.ThrowsAsync<TimeoutException>(() => client.GetAssetsAsync());

        // The timed-out request neither acquired a token nor released the lock it never held,
        // so the first request still completes normally.
        _tokens.CompleteFirstAcquisition();
        await first.WaitAsync(TimeSpan.FromSeconds(10));
        Assert.Equal(1, _tokens.AcquisitionCount);
        Assert.Equal(1, _api.CallCount);
    }

    /// <summary>A token provider whose first acquisition blocks until released; later ones complete at once.</summary>
    private sealed class BlockingAccessTokenProvider : IAccessTokenProvider
    {
        private readonly TaskCompletionSource _firstStarted = new(TaskCreationOptions.RunContinuationsAsynchronously);
        private readonly TaskCompletionSource _firstReleased = new(TaskCreationOptions.RunContinuationsAsynchronously);
        private int _acquisitionCount;

        public int AcquisitionCount => _acquisitionCount;

        public Task FirstAcquisitionStarted => _firstStarted.Task;

        public void CompleteFirstAcquisition() => _firstReleased.SetResult();

        public async Task AcquireTokenAsync(CancellationToken cancellationToken = default)
        {
            if (Interlocked.Increment(ref _acquisitionCount) == 1)
            {
                _firstStarted.SetResult();
                await _firstReleased.Task.WaitAsync(cancellationToken);
            }
        }

        public DateTimeOffset GetTokenExpiry() => DateTimeOffset.UtcNow.AddHours(1);

        public IDictionary<string, string> GetAccessHeaders() => new Dictionary<string, string>
        {
            { "Authorization", "Bearer test-token" },
            { "x-region", "eu" },
        };
    }
}
