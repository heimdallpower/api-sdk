using System.Net;
using HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses.Fakes;

namespace HeimdallPower.Api.Client.UnitTests.WhenHandlingErrorResponses;

/// <summary>
/// Verifies that problem details returned by the API are exposed as typed properties on
/// <see cref="HeimdallApiException"/>, and still mirrored into <see cref="Exception.Data"/> for older callers.
/// </summary>
[Trait("Category", "Unit")]
public class WhenApiReturnsProblemDetails
{
    private const string Url = "https://fake-api.example.com/v1/test";

    private const string ProblemJson = """
        {
          "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
          "title": "One or more validation errors occurred.",
          "detail": "The since parameter is invalid.",
          "instance": "/grid_insights/v1/lines/x/currents/latest",
          "status": 400,
          "errors": { "since": ["Must be an ISO 8601 timestamp."] }
        }
        """;

    [Fact]
    public async Task ShouldExposeProblemDetailsAsTypedProperties()
    {
        var client = HeimdallApiHttpClientFactory.Create(FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.BadRequest, ProblemJson));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() => client.GetAsync<string>(Url));

        Assert.Equal(HttpStatusCode.BadRequest, ex.StatusCode);
        Assert.Equal(Url, ex.RequestUrl);
        Assert.Equal("One or more validation errors occurred.", ex.Title);
        Assert.Equal("The since parameter is invalid.", ex.Detail);
        Assert.Equal("https://tools.ietf.org/html/rfc9110#section-15.5.1", ex.Type);
        Assert.Equal("/grid_insights/v1/lines/x/currents/latest", ex.Instance);
        Assert.Equal(["Must be an ISO 8601 timestamp."], ex.Errors["since"]);
    }

    [Fact]
    public async Task ShouldKeepMirroringProblemDetailsIntoExceptionData()
    {
        var client = HeimdallApiHttpClientFactory.Create(FakeHttpMessageHandler.ReturnsJson(HttpStatusCode.BadRequest, ProblemJson));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() => client.GetAsync<string>(Url));

        Assert.Equal("One or more validation errors occurred.", ex.Data["Title"]);
        Assert.Equal(Url, ex.Data["RequestUrl"]);
        Assert.Equal(new[] { "Must be an ISO 8601 timestamp." }, ex.Data["since"]);
    }

    [Fact]
    public async Task ShouldHaveEmptyErrorsAndNullDetails_WhenBodyIsNotProblemDetails()
    {
        var client = HeimdallApiHttpClientFactory.Create(FakeHttpMessageHandler.ReturnsHtml(HttpStatusCode.BadGateway));

        var ex = await Assert.ThrowsAsync<HeimdallApiException>(() => client.GetAsync<string>(Url));

        Assert.Empty(ex.Errors);
        Assert.Null(ex.Title);
        Assert.Equal(Url, ex.RequestUrl);
    }
}
