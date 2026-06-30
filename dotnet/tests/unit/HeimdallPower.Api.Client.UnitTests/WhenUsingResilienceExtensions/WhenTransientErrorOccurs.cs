using System.Net;
using HeimdallPower.Api.Client.Extensions;
using HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions.Fakes;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Http.Resilience;
using Microsoft.Extensions.Logging;
using Polly;

namespace HeimdallPower.Api.Client.UnitTests.WhenUsingResilienceExtensions;

/// <summary>
/// Verifies the retry behaviour of the resilience pipeline wired up by
/// <see cref="HeimdallApiClientExtensions.AddHeimdallPowerApiClient"/>.
///
/// <para>
/// <see cref="WhenStandardResilienceHandlerIsConfigured"/> uses <c>AddStandardResilienceHandler</c>
/// configured with zero delays to exhaustively verify which HTTP status codes are retried.
/// These tests run instantly and mirror the exact pipeline that <c>AddHeimdallPowerApiClient</c> registers.
/// </para>
///
/// <para>
/// <see cref="WhenAddHeimdallPowerApiClientIsRegistered"/> is a smoke-test that uses the real DI
/// registration to confirm retries are present end-to-end (real backoff delays apply, ~10 s).
/// </para>
/// </summary>
public static class WhenTransientErrorOccurs
{
    // ─────────────────────────────────────────────────────────────────────────
    // Fast tests — AddStandardResilienceHandler with zero-delay retry
    // (mirrors the pipeline registered by AddHeimdallPowerApiClient)
    // ─────────────────────────────────────────────────────────────────────────

    [Trait("Category", "Unit")]
    public class WhenStandardResilienceHandlerIsConfigured
    {
        /// <summary>
        /// Builds a provider with <c>AddStandardResilienceHandler</c> configured for zero-delay
        /// retries. This mirrors what <see cref="HeimdallApiClientExtensions.AddHeimdallPowerApiClient"/>
        /// registers, but with delays removed so tests run instantly.
        /// </summary>
        private static ServiceProvider BuildProvider(CountingHttpMessageHandler fakeHandler) =>
            BuildProviderWithReturnFunc(_ => fakeHandler);

        private static ServiceProvider BuildProviderWithReturnFunc(Func<IServiceProvider, HttpMessageHandler> handlerFactory)
        {
            var services = new ServiceCollection();
            services.AddLogging(b => b.AddDebug());

            services.AddHttpClient("HeimdallPower")
                .ConfigurePrimaryHttpMessageHandler(handlerFactory)
                .AddStandardResilienceHandler(o =>
                {
                    // Zero delays: tests run instantly while still exercising the full retry pipeline.
                    o.Retry.Delay = TimeSpan.Zero;
                    o.Retry.BackoffType = DelayBackoffType.Constant;
                    o.Retry.UseJitter = false;
                    o.Retry.MaxRetryAttempts = 3;
                    // Keep timeouts generous so the fake handler is never timed-out.
                    o.AttemptTimeout.Timeout = TimeSpan.FromSeconds(10);
                    o.TotalRequestTimeout.Timeout = TimeSpan.FromSeconds(60);
                    // Raise threshold so the circuit breaker stays closed during tests.
                    o.CircuitBreaker.MinimumThroughput = 100;
                });

            return services.BuildServiceProvider();
        }

        // ── Transient status codes that SHOULD be retried ──────────────────

        [Theory]
        [InlineData(HttpStatusCode.BadGateway)]          // 502
        [InlineData(HttpStatusCode.ServiceUnavailable)]  // 503
        [InlineData(HttpStatusCode.GatewayTimeout)]      // 504
        [InlineData(HttpStatusCode.InternalServerError)] // 500
        public async Task ShouldRetry_WhenTransientStatusCodeReturned(HttpStatusCode statusCode)
        {
            var handler = new CountingHttpMessageHandler(_ => new HttpResponseMessage(statusCode));
            var provider = BuildProvider(handler);
            var client = provider.GetRequiredService<IHttpClientFactory>().CreateClient("HeimdallPower");

            await client.GetAsync("https://test.example.com/api/test");

            // 1 initial attempt + 3 retries = 4 total calls
            Assert.Equal(4, handler.CallCount);
        }

        [Fact]
        public async Task ShouldRetry_WhenHttpRequestExceptionThrown()
        {
            var handler = new CountingHttpMessageHandler(_ => throw new HttpRequestException("Connection refused"));
            var provider = BuildProvider(handler);
            var client = provider.GetRequiredService<IHttpClientFactory>().CreateClient("HeimdallPower");

            // All retries exhausted → exception propagates to caller
            await Assert.ThrowsAnyAsync<Exception>(() =>
                client.GetAsync("https://test.example.com/api/test"));

            Assert.Equal(4, handler.CallCount);
        }

        // ── Permanent status codes that should NOT be retried ───────────────

        [Theory]
        [InlineData(HttpStatusCode.BadRequest)]   // 400
        [InlineData(HttpStatusCode.Unauthorized)] // 401
        [InlineData(HttpStatusCode.Forbidden)]    // 403
        [InlineData(HttpStatusCode.NotFound)]     // 404
        public async Task ShouldNotRetry_WhenPermanentStatusCodeReturned(HttpStatusCode statusCode)
        {
            var handler = new CountingHttpMessageHandler(_ => new HttpResponseMessage(statusCode));
            var provider = BuildProvider(handler);
            var client = provider.GetRequiredService<IHttpClientFactory>().CreateClient("HeimdallPower");

            await client.GetAsync("https://test.example.com/api/test");

            Assert.Equal(1, handler.CallCount);
        }

        // ── Transparent success after transient failure ─────────────────────

        [Theory]
        [InlineData(HttpStatusCode.BadGateway)]
        [InlineData(HttpStatusCode.ServiceUnavailable)]
        [InlineData(HttpStatusCode.GatewayTimeout)]
        public async Task ShouldSucceed_WhenTransientErrorRecoveredOnSecondAttempt(HttpStatusCode transientCode)
        {
            var callCount = 0;
            var handler = new CountingHttpMessageHandler(_ =>
            {
                callCount++;
                return callCount == 1
                    ? new HttpResponseMessage(transientCode)
                    : new HttpResponseMessage(HttpStatusCode.OK);
            });

            var provider = BuildProvider(handler);
            var client = provider.GetRequiredService<IHttpClientFactory>().CreateClient("HeimdallPower");

            var response = await client.GetAsync("https://test.example.com/api/test");

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.Equal(2, handler.CallCount);
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Smoke test — AddHeimdallPowerApiClient uses AddStandardResilienceHandler
    // Note: real backoff applies here (~10 s per retry-exhaustion scenario).
    // ─────────────────────────────────────────────────────────────────────────

    [Trait("Category", "Unit")]
    public class WhenAddHeimdallPowerApiClientIsRegistered
    {
        [Theory]
        [InlineData(HttpStatusCode.BadGateway)]
        [InlineData(HttpStatusCode.ServiceUnavailable)]
        [InlineData(HttpStatusCode.GatewayTimeout)]
        public async Task ShouldRetry_WhenTransientGatewayErrorOccurs(HttpStatusCode statusCode)
        {
            // One transient error followed by success — verifies that retries are wired up
            // without requiring all 3 retries to be exhausted (keeps the test < 5 s).
            var callCount = 0;
            var handler = new CountingHttpMessageHandler(_ =>
            {
                callCount++;
                return callCount == 1
                    ? new HttpResponseMessage(statusCode)
                    : new HttpResponseMessage(HttpStatusCode.OK);
            });

            var services = new ServiceCollection();
            services.AddLogging(b => b.AddDebug());
            services.AddHeimdallPowerApiClient(o =>
            {
                o.ClientId = "test-id";
                o.ClientSecret = "test-secret";
            });
            services.AddHttpClient("HeimdallPower")
                .ConfigurePrimaryHttpMessageHandler(() => handler);

            var provider = services.BuildServiceProvider();
            var client = provider.GetRequiredService<IHttpClientFactory>().CreateClient("HeimdallPower");

            var response = await client.GetAsync("https://test.example.com/api/test");

            Assert.Equal(HttpStatusCode.OK, response.StatusCode);
            Assert.Equal(2, callCount);
        }
    }
}



