namespace HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;

/// <summary>
/// A fake <see cref="HttpMessageHandler"/> that invokes a delegate for each request
/// and tracks the total number of attempts (including retries).
/// </summary>
internal sealed class CountingHttpMessageHandler(Func<HttpRequestMessage, HttpResponseMessage> respond) : HttpMessageHandler
{
    public int CallCount { get; private set; }

    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
    {
        CallCount++;
        return Task.FromResult(respond(request));
    }
}

