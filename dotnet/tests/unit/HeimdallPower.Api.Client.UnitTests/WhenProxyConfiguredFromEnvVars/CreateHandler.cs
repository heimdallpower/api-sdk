using System.Net;
using HeimdallPower.Api.Client.Extensions;

namespace HeimdallPower.Api.Client.UnitTests.WhenProxyConfiguredFromEnvVars;

[Trait("Category", "Unit")]
public class CreateHandler(CreateHandler.Scenario scenario)
    : IClassFixture<CreateHandler.Scenario>, IDisposable
{
    public class Scenario : IDisposable
    {
        public WebProxy Proxy { get; }

        public Scenario()
        {
            ClearEnvVars();
            Environment.SetEnvironmentVariable("HTTPS_PROXY", "http://https-proxy:3128");
            Environment.SetEnvironmentVariable("HTTP_PROXY", "http://http-proxy:3128");
            Environment.SetEnvironmentVariable("NO_PROXY", ".env-domain.com,localhost");

            var handler = ProxyHandlerFactory.CreateHandler(new ProxyOptions
            {
                UseEnvironmentVariables = true,
                BypassList = ["*.internal.com"]
            })!;
            Proxy = (WebProxy)handler.Proxy!;
        }

        public void Dispose() => ClearEnvVars();

        private static void ClearEnvVars()
        {
            foreach (var key in new[] { "HTTPS_PROXY", "https_proxy", "HTTP_PROXY", "http_proxy", "NO_PROXY", "no_proxy" })
                Environment.SetEnvironmentVariable(key, null);
        }
    }

    public void Dispose() => scenario.Dispose();

    [Fact]
    public void ShouldPreferHttpsProxy()
    {
        Assert.Equal(new Uri("http://https-proxy:3128"), scenario.Proxy.Address);
    }

    [Fact]
    public void ShouldMergeBypassListFromOptionsAndNoProxy()
    {
        Assert.Equal(3, scenario.Proxy.BypassList.Length);
    }
}
