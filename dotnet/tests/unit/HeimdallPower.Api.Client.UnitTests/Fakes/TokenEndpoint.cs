using System.IdentityModel.Tokens.Jwt;
using System.Net;
using System.Net.Sockets;
using System.Security.Claims;
using System.Text;

namespace HeimdallPower.Api.Client.UnitTests.Fakes;

/// <summary>
/// Responses from the access token endpoint, for tests that exercise real token acquisition
/// over a fake transport.
/// </summary>
internal static class TokenEndpoint
{
    /// <summary>An unsigned JWT carrying the <c>region</c> claim the client reads.</summary>
    public static readonly string AccessToken =
        new JwtSecurityTokenHandler().WriteToken(new JwtSecurityToken(claims: [new Claim("region", "eu")]));

    public static HttpResponseMessage Token() =>
        Json(HttpStatusCode.OK, $$"""{"access_token":"{{AccessToken}}","token_type":"Bearer","expires_in":3600}""");

    public static HttpResponseMessage Error(HttpStatusCode statusCode, string error) =>
        Json(statusCode, $$"""{"error":"{{error}}","error_description":"Token request failed."}""");

    /// <summary>The exception a dropped connection surfaces as ("Connection reset by peer").</summary>
    public static HttpRequestException ConnectionReset() =>
        new("An error occurred while sending the request.",
            new IOException("Unable to read data from the transport connection: Connection reset by peer.",
                new SocketException((int)SocketError.ConnectionReset)));

    /// <summary>The exception <see cref="HttpClient"/> throws when its <see cref="HttpClient.Timeout"/> elapses.</summary>
    public static TaskCanceledException TimedOut() =>
        new("The request was canceled due to the configured HttpClient.Timeout of 100 seconds elapsing.",
            new TimeoutException("A task was canceled."));

    private static HttpResponseMessage Json(HttpStatusCode statusCode, string json) =>
        new(statusCode) { Content = new StringContent(json, Encoding.UTF8, "application/json") };
}
