using HeimdallPower.Api.Client.Common;
using StreamUrlBuilder = HeimdallPower.Api.Client.Stream.StreamUrlBuilder;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming;

/// <summary>
/// Verifies the URL built for the Heimdall Stream API's SSE endpoint.
/// </summary>
[Trait("Category", "Unit")]
public class WhenBuildingUrls
{
    [Fact]
    public void ShouldBuildUrlWithoutQueryString_WhenQuantityIsDefault()
    {
        var url = StreamUrlBuilder.BuildStreamUrl(version: 1);

        Assert.Equal("/v1/stream", url);
    }

    [Fact]
    public void ShouldIncludeQuantity_WhenNotCurrent()
    {
        var url = StreamUrlBuilder.BuildStreamUrl(version: 1, quantity: Quantity.ApparentPower);

        Assert.Equal("/v1/stream?quantity=apparent_power", url);
    }

    [Fact]
    public void ShouldOmitQuantity_WhenCurrent()
    {
        var url = StreamUrlBuilder.BuildStreamUrl(version: 1, quantity: Quantity.Current);

        Assert.Equal("/v1/stream", url);
    }

    [Fact]
    public void ShouldUseGivenVersion()
    {
        var url = StreamUrlBuilder.BuildStreamUrl(version: 2);

        Assert.Equal("/v2/stream", url);
    }
}
