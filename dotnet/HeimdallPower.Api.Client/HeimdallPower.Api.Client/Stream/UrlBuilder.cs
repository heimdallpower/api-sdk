using System.Collections.Specialized;
using HeimdallPower.Api.Client.Stream.CapacityMonitoring;

namespace HeimdallPower.Api.Client.Stream;

internal static class UrlBuilder
{
    private const string Stream = "stream";

    public static string BuildStreamUrl(int version, Guid? gridOwnerId, Quantity quantity = Quantity.Current)
    {
        var queryParams = new NameValueCollection();

        if (gridOwnerId.HasValue)
            queryParams.AddQueryParam("gridownerid", gridOwnerId.Value.ToString());

        if (quantity != Quantity.Current)
            queryParams.AddQueryParam("quantity", quantity.ToQueryValue());

        var url = $"/v{version}/{Stream}";

        return queryParams.Count > 0 ? url + queryParams.ToQueryString() : url;
    }
}
