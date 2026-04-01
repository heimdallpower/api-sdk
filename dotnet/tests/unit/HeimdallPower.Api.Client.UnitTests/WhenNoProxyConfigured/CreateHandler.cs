using HeimdallPower.Api.Client.Extensions;

namespace HeimdallPower.Api.Client.UnitTests.WhenNoProxyConfigured;

[Trait("Category", "Unit")]
public class CreateHandler
{
    [Fact]
    public void ShouldReturnNull_WhenOptionsIsNull()
    {
        Assert.Null(ProxyHandlerFactory.CreateHandler(null));
    }

    [Fact]
    public void ShouldReturnNull_WhenNoAddressAndEnvVarsDisabled()
    {
        Assert.Null(ProxyHandlerFactory.CreateHandler(new ProxyOptions { UseEnvironmentVariables = false }));
    }
}
