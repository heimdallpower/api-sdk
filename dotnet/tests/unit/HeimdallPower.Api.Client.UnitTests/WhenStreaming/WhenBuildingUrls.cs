using HeimdallPower.Api.Client.Stream.CapacityMonitoring;
using StreamUrlBuilder = HeimdallPower.Api.Client.Stream.UrlBuilder;

namespace HeimdallPower.Api.Client.UnitTests.WhenStreaming;

/// <summary>
/// Verifies the URL built for the Heimdall Stream API's SSE endpoint.
/// </summary>
[Trait("Category", "Unit")]
public class WhenBuildingUrls
{
    [Fact]
    public void ShouldBuildUrlWithoutQueryString_WhenGridOwnerIdIsNullAndQuantityIsDefault()
    {
        var url = StreamUrlBuilder.BuildStreamUrl(version: 1, gridOwnerId: null);

        Assert.Equal("/v1/stream", url);
    }

    [Fact]
    public void ShouldIncludeGridOwnerId_WhenProvided()
    {
        var gridOwnerId = Guid.NewGuid();

        var url = StreamUrlBuilder.BuildStreamUrl(version: 1, gridOwnerId: gridOwnerId);

        Assert.Equal($"/v1/stream?gridownerid={gridOwnerId}", url);
    }

    [Fact]
    public void ShouldIncludeQuantity_WhenNotCurrent()
    {
        var url = StreamUrlBuilder.BuildStreamUrl(version: 1, gridOwnerId: null, quantity: Quantity.ApparentPower);

        Assert.Equal("/v1/stream?quantity=apparent_power", url);
    }

    [Fact]
    public void ShouldOmitQuantity_WhenCurrent()
    {
        var gridOwnerId = Guid.NewGuid();

        var url = StreamUrlBuilder.BuildStreamUrl(version: 1, gridOwnerId: gridOwnerId, quantity: Quantity.Current);

        Assert.Equal($"/v1/stream?gridownerid={gridOwnerId}", url);
    }

    [Fact]
    public void ShouldIncludeBothGridOwnerIdAndQuantity_WhenBothProvided()
    {
        var gridOwnerId = Guid.NewGuid();

        var url = StreamUrlBuilder.BuildStreamUrl(version: 1, gridOwnerId: gridOwnerId, quantity: Quantity.ApparentPower);

        Assert.Equal($"/v1/stream?gridownerid={gridOwnerId}&quantity=apparent_power", url);
    }

    [Fact]
    public void ShouldUseGivenVersion()
    {
        var url = StreamUrlBuilder.BuildStreamUrl(version: 2, gridOwnerId: null);

        Assert.Equal("/v2/stream", url);
    }
}
