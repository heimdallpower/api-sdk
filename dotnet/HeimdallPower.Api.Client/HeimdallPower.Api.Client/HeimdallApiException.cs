using System.Net;

namespace HeimdallPower.Api.Client;

public class HeimdallApiException : Exception
{
    public HttpStatusCode StatusCode { get; }

    public HeimdallApiException(string message, HttpStatusCode statusCode, string requestUrl = "")
        : base(message)
    {
        StatusCode = statusCode;
        base.Data["RequestUrl"] = requestUrl;
    }

    public HeimdallApiException(ProblemDetails problemDetails, HttpStatusCode statusCode, string requestUrl = "")
        : base(problemDetails.Detail ?? "An error occurred while processing the request.")
    {
        StatusCode = statusCode;
        base.Data["RequestUrl"] = requestUrl;
        base.Data["Title"] = problemDetails.Title;
        base.Data["Instance"] = problemDetails.Instance;
        base.Data["Type"] = problemDetails.Type;
        if (problemDetails.Errors == null) return;
        foreach (var error in problemDetails.Errors)
        {
            base.Data[error.Key] = error.Value;
        }
    }
}
