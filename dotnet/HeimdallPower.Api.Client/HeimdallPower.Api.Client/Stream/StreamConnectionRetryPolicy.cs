namespace HeimdallPower.Api.Client.Stream;

/// <summary>
/// Configures the exponential backoff (with jitter) used between stream reconnect attempts.
/// </summary>
public sealed class StreamConnectionRetryPolicyOptions
{
    /// <summary>
    /// The delay before the first reconnect attempt. Defaults to 1 second.
    /// </summary>
    public TimeSpan? InitialDelay { get; init; }

    /// <summary>
    /// The maximum delay between reconnect attempts. Defaults to 30 seconds.
    /// </summary>
    public TimeSpan? MaxDelay { get; init; }

    /// <summary>
    /// The maximum number of consecutive reconnect attempts before giving up. Defaults to 5.
    /// </summary>
    public int? MaxRetries { get; init; }
}

/// <summary>
/// Computes the exponential backoff (with jitter) delay between stream reconnect attempts.
/// Also holds the configured maximum number of retries before giving up.
/// </summary>
internal sealed class StreamConnectionRetryPolicy(StreamConnectionRetryPolicyOptions? options = null)
{
    private readonly TimeSpan _initialDelay = options?.InitialDelay ?? TimeSpan.FromSeconds(1);
    private readonly TimeSpan _maxDelay = options?.MaxDelay ?? TimeSpan.FromSeconds(30);
    private readonly int _maxRetries = options?.MaxRetries ?? 5;

    /// <summary>
    /// Gets the delay to wait before the next reconnect attempt.
    /// </summary>
    /// <param name="failedAttempts">The number of consecutive failed connection attempts so far.</param>
    /// <returns>The backoff delay, with jitter applied, capped at the configured maximum delay.</returns>
    public TimeSpan GetDelay(int failedAttempts)
    {
        if (failedAttempts <= 1)
            return _initialDelay;

        var exponential = _initialDelay * Math.Pow(2, Math.Min(failedAttempts, 10));
        var capped = exponential < _maxDelay ? exponential : _maxDelay;

        // Jitter avoids a thundering herd of clients reconnecting simultaneously.
        return capped * (0.8 + (Random.Shared.NextDouble() * 0.4));
    }

    /// <summary>
    /// Determines whether another retry attempt should be made based on the number of failed attempts.
    /// </summary>
    /// <param name="failedAttempts">The number of consecutive failed connection attempts so far.</param>
    /// <returns><c>true</c> if another retry should be attempted; otherwise, <c>false</c>.</returns>
    public bool ShouldRetry(int failedAttempts)
    {
        return failedAttempts <= _maxRetries;
    }
}
