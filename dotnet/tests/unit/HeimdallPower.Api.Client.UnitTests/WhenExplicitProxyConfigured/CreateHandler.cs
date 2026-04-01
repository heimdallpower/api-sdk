using System.Net;
using HeimdallPower.Api.Client.Extensions;

namespace HeimdallPower.Api.Client.UnitTests.WhenExplicitProxyConfigured;

[Trait("Category", "Unit")]
public class CreateHandler(CreateHandler.Scenario scenario)
    : IClassFixture<CreateHandler.Scenario>
{
    public class Scenario
    {
        public HttpClientHandler Handler { get; }
        public WebProxy Proxy { get; }

        public Scenario()
        {
            Handler = ProxyHandlerFactory.CreateHandler(new ProxyOptions
            {
                Address = "http://proxy:8080",
                Username = "user",
                Password = "pass",
                BypassList = ["*.internal.com"],
                UseEnvironmentVariables = false
            })!;
            Proxy = (WebProxy)Handler.Proxy!;
        }
    }

    [Fact]
    public void ShouldEnableProxy()
    {
        Assert.True(scenario.Handler.UseProxy);
    }

    [Fact]
    public void ShouldSetProxyAddress()
    {
        Assert.Equal(new Uri("http://proxy:8080"), scenario.Proxy.Address);
    }

    [Fact]
    public void ShouldSetCredentials()
    {
        var creds = (NetworkCredential)scenario.Proxy.Credentials!;
        Assert.Equal("user", creds.UserName);
        Assert.Equal("pass", creds.Password);
    }

    [Fact]
    public void ShouldSetBypassList()
    {
        Assert.Single(scenario.Proxy.BypassList);
    }
}
