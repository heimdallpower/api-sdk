namespace HeimdallPower.Api.Client.CapacityMonitoring.Lines;

public record LatestLineTransientRatingResponse
{
    /// <summary>
    /// A human-readable label identifying the rating returned by this endpoint, independent of the quantity parameter.
    /// </summary>
    /// <example>Line transient rating</example>
    public required string Metric { get; init; }

    /// <summary>
    /// The unit of the values in the response. Depends on the requested quantity:
    /// "Ampere" for current (default), "MVA" for apparent_power.
    /// </summary>
    /// <example>Ampere</example>
    public required string Unit { get; init; }

    /// <summary>
    /// The line transient rating with timestamp and one value per calculated duration.
    /// </summary>
    public required LineTransientRatingDto LineTransientRating { get; init; }
}
