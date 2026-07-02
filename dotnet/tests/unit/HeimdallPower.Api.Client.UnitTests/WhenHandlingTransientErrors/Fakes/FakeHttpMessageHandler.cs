namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingTransientErrors.Fakes;

/// <summary>
/// A minimal <see cref="HttpMessageHandler"/> for unit tests that returns
/// a fixed response or a pre-configured sequence of responses.
/// </summary>
internal sealed class FakeHttpMessageHandler : HttpMessageHandler
{
    private readonly Queue<HttpResponseMessage> _responses;
    private readonly HttpResponseMessage _last;

    /// <summary>Returns <paramref name="response"/> for every request.</summary>
    public FakeHttpMessageHandler(HttpResponseMessage response)
    {
        _responses = new Queue<HttpResponseMessage>();
        _last = response;
    }

    /// <summary>
    /// Returns responses from <paramref name="responses"/> in order.
    /// Once the queue is exhausted the last response is repeated.
    /// </summary>
    public FakeHttpMessageHandler(params HttpResponseMessage[] responses)
    {
        if (responses.Length == 0) throw new ArgumentException("At least one response is required.", nameof(responses));
        _last = responses[^1];
        _responses = new Queue<HttpResponseMessage>(responses[..^1]);
    }

    protected override Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request,
        CancellationToken cancellationToken)
    {
        var response = _responses.Count > 0 ? _responses.Dequeue() : _last;
        response.RequestMessage = request;
        return Task.FromResult(response);
    }
}

