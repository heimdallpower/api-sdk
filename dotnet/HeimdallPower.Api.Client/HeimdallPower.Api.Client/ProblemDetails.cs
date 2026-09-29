namespace HeimdallPower.Api.Client;

internal class ProblemDetails
{
    public string? Title { get; init; }
    public string? Detail { get; init; }
    public string? Instance { get; init; }
    public string? Type { get; init; }
    public IDictionary<string, string[]>? Errors { get; init; }
}
