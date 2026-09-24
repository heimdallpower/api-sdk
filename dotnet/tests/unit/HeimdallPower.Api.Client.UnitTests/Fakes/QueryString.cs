using System.Collections.Specialized;
using System.Web;

namespace HeimdallPower.Api.Client.UnitTests.Fakes;

internal static class QueryString
{
    public static NameValueCollection Of(HttpRequestMessage request) =>
        HttpUtility.ParseQueryString(request.RequestUri!.Query);
}
