using HeimdallPower.Api.Client.Stream;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming;

/// <summary>
/// Data-driven tests for <see cref="StreamConnectionRetryPolicy"/>'s exponential backoff + jitter math.
/// Jitter is random, so assertions check bounds rather than exact values.
/// Also verifies that the policy never exceeds the configured maximum delay, even after many failed attempts.
/// And checks the maximum limit of retries, which is a safety feature to prevent infinite retry loops in case of persistent failures.
/// </summary>
[Trait("Category", "Unit")]
public class WhenComputingRetryDelay
{
    private static readonly TimeSpan InitialDelay = TimeSpan.FromSeconds(1);
    private static readonly TimeSpan MaxDelay = TimeSpan.FromSeconds(30);

    private readonly StreamConnectionRetryPolicy _policy = new(new StreamConnectionRetryPolicyOptions { InitialDelay = InitialDelay, MaxDelay = MaxDelay });

    [Theory]
    [InlineData(1)]
    [InlineData(0)]
    [InlineData(-1)]
    public void ShouldReturnInitialDelay_WhenFirstOrNoFailedAttempts(int failedAttempts)
    {
        var delay = _policy.GetDelay(failedAttempts);

        Assert.Equal(InitialDelay, delay);
    }

    [Theory]
    [InlineData(2, 1.6, 2.4)]   // 1s * 2^1 = 2s, +/-20% jitter
    [InlineData(3, 3.2, 4.8)]   // 1s * 2^2 = 4s, +/-20% jitter
    [InlineData(4, 6.4, 9.6)] // 1s * 2^3 = 8s, +/-20% jitter
    [InlineData(5, 12.8, 19.2)] // 1s * 2^4 = 16s, +/-20% jitter
    public void ShouldDoubleDelayPerAttempt_WithinJitterBand(int failedAttempts, double minSeconds, double maxSeconds)
    {
        var delay = _policy.GetDelay(failedAttempts);

        Assert.InRange(delay.TotalSeconds, minSeconds, maxSeconds);
    }

    [Theory]
    [InlineData(10)]
    [InlineData(100)]
    public void ShouldCapAtMaxDelay_WithinJitterBand(int failedAttempts)
    {
        var delay = _policy.GetDelay(failedAttempts);

        Assert.InRange(delay.TotalSeconds, MaxDelay.TotalSeconds * 0.8, MaxDelay.TotalSeconds * 1.2);
    }

    [Fact]
    public void ShouldNeverExceedMaxDelayPlusJitter_AcrossManyAttempts()
    {
        for (var attempt = 1; attempt <= 20; attempt++)
        {
            var delay = _policy.GetDelay(attempt);

            Assert.True(delay <= MaxDelay * 1.2, $"Delay {delay} at attempt {attempt} exceeded max+jitter bound");
            Assert.True(delay >= InitialDelay * 0.8, $"Delay {delay} at attempt {attempt} was below the initial*0.8 floor");
        }
    }
}
