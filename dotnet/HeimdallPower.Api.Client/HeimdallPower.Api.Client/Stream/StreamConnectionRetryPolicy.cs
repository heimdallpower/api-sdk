namespace HeimdallPower.Api.Client.Stream;

/// <summary>
/// Computes the exponential backoff (with jitter) delay between stream reconnect attempts.
/// </summary>
internal sealed class StreamConnectionRetryPolicy(TimeSpan? initialDelay = null, TimeSpan? maxDelay = null)
{
    private readonly TimeSpan _initialDelay = initialDelay ?? TimeSpan.FromSeconds(1);
    private readonly TimeSpan _maxDelay = maxDelay ?? TimeSpan.FromSeconds(30);

    public TimeSpan GetDelay(int failedAttempts)
    {
        if (failedAttempts <= 0)
            return _initialDelay;

        var exponential = _initialDelay * Math.Pow(2, Math.Min(failedAttempts, 10));
        var capped = exponential < _maxDelay ? exponential : _maxDelay;

        // Jitter avoids a thundering herd of clients reconnecting simultaneously.
        return capped * (0.8 + (Random.Shared.NextDouble() * 0.4));
    }
}
