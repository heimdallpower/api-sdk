using HeimdallPower.Api.Client.Common;
using System.Collections.Specialized;

namespace HeimdallPower.Api.Client.Stream;

internal static class StreamUrlBuilder
{
    private const string StreamPath = "stream";

    public static string BuildStreamUrl(int version, Quantity quantity = Quantity.Current)
    {
        var queryParams = new NameValueCollection();

        if (quantity != Quantity.Current)
            queryParams.AddQueryParam("quantity", quantity.ToQueryValue());

        var url = $"/v{version}/{StreamPath}";

        return queryParams.Count > 0 ? url + queryParams.ToQueryString() : url;
    }
}
