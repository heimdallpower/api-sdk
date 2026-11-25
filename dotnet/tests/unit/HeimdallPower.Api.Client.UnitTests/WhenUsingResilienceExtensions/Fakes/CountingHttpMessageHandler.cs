namespace HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

/// <summary>
/// A fake <see cref="HttpMessageHandler"/> that invokes a delegate for each request
/// and tracks the total number of attempts (including retries).
/// </summary>
internal sealed class CountingHttpMessageHandler(Func<HttpRequestMessage, CancellationToken, Task<HttpResponseMessage>> respond) : HttpMessageHandler
{
    private int _callCount;

    public CountingHttpMessageHandler(Func<HttpRequestMessage, HttpResponseMessage> respond)
        : this((request, _) => Task.FromResult(respond(request)))
    {
    }

    public int CallCount => _callCount;

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        Interlocked.Increment(ref _callCount);
        return respond(request, cancellationToken);
    }
}
