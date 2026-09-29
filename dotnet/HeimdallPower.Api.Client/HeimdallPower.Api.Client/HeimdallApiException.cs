using System.Collections.ObjectModel;
using System.Net;

namespace HeimdallPower.Api.Client;

/// <summary>
/// Thrown when the Heimdall Power API responds with a non-success status code.
/// When the API returns an RFC 7807 problem details body, its fields are exposed as typed properties.
/// </summary>
public class HeimdallApiException : Exception
{
    /// <summary>
    /// The HTTP status code returned by the API.
    /// </summary>
    public HttpStatusCode StatusCode { get; }

    /// <summary>
    /// The URL of the request that failed. Empty when unknown.
    /// </summary>
    public string RequestUrl { get; }

    /// <summary>
    /// Short, human-readable summary of the problem, if the API returned one.
    /// </summary>
    public string? Title { get; }

    /// <summary>
    /// Human-readable explanation specific to this occurrence of the problem, if the API returned one.
    /// </summary>
    public string? Detail { get; }

    /// <summary>
    /// URI reference identifying the problem type, if the API returned one.
    /// </summary>
    public string? Type { get; }

    /// <summary>
    /// URI reference identifying this specific occurrence of the problem, if the API returned one.
    /// </summary>
    public string? Instance { get; }

    /// <summary>
    /// Validation errors keyed by the offending field. Empty when the API returned none.
    /// </summary>
    public IReadOnlyDictionary<string, string[]> Errors { get; }

    /// <summary>
    /// Creates an exception without problem details. Public so consumers can throw it from test doubles.
    /// </summary>
    /// <param name="message">The error message.</param>
    /// <param name="statusCode">The HTTP status code returned by the API.</param>
    /// <param name="requestUrl">The URL of the request that failed.</param>
    public HeimdallApiException(string message, HttpStatusCode statusCode, string requestUrl = "")
        : base(message)
    {
        StatusCode = statusCode;
        RequestUrl = requestUrl;
        Errors = ReadOnlyDictionary<string, string[]>.Empty;
        base.Data["RequestUrl"] = requestUrl;
    }

    internal HeimdallApiException(ProblemDetails problemDetails, HttpStatusCode statusCode, string requestUrl = "")
        : base(problemDetails.Detail ?? "An error occurred while processing the request.")
    {
        StatusCode = statusCode;
        RequestUrl = requestUrl;
        Title = problemDetails.Title;
        Detail = problemDetails.Detail;
        Type = problemDetails.Type;
        Instance = problemDetails.Instance;
        Errors = problemDetails.Errors is { } errors ? new ReadOnlyDictionary<string, string[]>(errors) : ReadOnlyDictionary<string, string[]>.Empty;

        // Kept for callers that read the untyped Exception.Data bag from earlier versions.
        base.Data["RequestUrl"] = requestUrl;
        base.Data["Title"] = problemDetails.Title;
        base.Data["Instance"] = problemDetails.Instance;
        base.Data["Type"] = problemDetails.Type;
        foreach (var error in Errors)
        {
            base.Data[error.Key] = error.Value;
        }
    }
}
