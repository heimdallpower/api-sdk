using System.Net;

namespace HeimdallPower.Api.Client.IntegrationTests.WhenAuthenticated;

[Trait("Category", "Integration")]
public class InspectHeaders(InspectHeaders.Scenario scenario) : IClassFixture<InspectHeaders.Scenario>
{
    public class Scenario : AuthenticatedHeimdallApiClient
    {
        public HttpRequestMessage? CapturedRequest { get; private set; }

        public Scenario()
        {
            // Create a capturing handler that records the outgoing request headers
            // then delegates to the real HTTP stack
            var capturingHandler = new CapturingDelegatingHandler();
            var httpClient = new HttpClient(capturingHandler)
            {
                BaseAddress = new Uri("https://external-api.heimdallcloud.com")
            };

            var clientSecret = Environment.GetEnvironmentVariable("HEIMDALL_CLIENT_SECRET")
                ?? throw new InvalidOperationException("HEIMDALL_CLIENT_SECRET environment variable is not set.");
            var clientId = Environment.GetEnvironmentVariable("HEIMDALL_CLIENT_ID")
                ?? throw new InvalidOperationException("HEIMDALL_CLIENT_ID environment variable is not set.");

            var client = new HeimdallApiClient(clientId, clientSecret, httpClient);

            try
            {
                client.GetAssetsAsync().GetAwaiter().GetResult();
            }
            catch
            {
                // We only care about capturing the request, not the response
            }

            CapturedRequest = capturingHandler.LastRequest;
        }
    }

    [Fact]
    public void RequestShouldContainXRegionHeader()
    {
        Assert.NotNull(scenario.CapturedRequest);
        Assert.True(
            scenario.CapturedRequest.Headers.Contains("x-region"),
            "Request should contain 'x-region' header");
    }

    [Fact]
    public void RequestShouldNotContainRegionHeaderWithoutPrefix()
    {
        Assert.NotNull(scenario.CapturedRequest);
        Assert.False(
            scenario.CapturedRequest.Headers.Contains("Region"),
            "Request should not contain 'Region' header (should be 'x-region')");
    }

    [Fact]
    public void XRegionHeaderShouldHaveValue()
    {
        Assert.NotNull(scenario.CapturedRequest);
        var regionValue = scenario.CapturedRequest.Headers.GetValues("x-region").Single();
        Assert.False(string.IsNullOrEmpty(regionValue), "x-region header should have a non-empty value");
    }

    private class CapturingDelegatingHandler() : DelegatingHandler(new HttpClientHandler())
    {
        public HttpRequestMessage? LastRequest { get; private set; }

        protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken cancellationToken)
        {
            LastRequest = request;
            return base.SendAsync(request, cancellationToken);
        }
    }
}
