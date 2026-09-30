namespace HeimdallPower.Api.Client.Assets;

public static class AssetsResponseExtensions
{
    /// <summary>
    /// Get all available lines
    /// </summary>
    /// <param name="response"></param>
    /// <returns></returns>
    public static IReadOnlyList<LineDto> AllLines(this AssetsResponse response)
    {
        return response.GridOwners
            .Where(go => go?.Facilities is { Count: > 0 })
            .SelectMany(go => go.Facilities
                .Where(facility => facility?.Line != null)
                .Select(facility => facility.Line!))
            .ToList();
    }

    /// <summary>
    /// Get all available facilities
    /// </summary>
    /// <param name="response"></param>
    /// <returns></returns>
    public static IReadOnlyList<FacilityDto> AllFacilities(this AssetsResponse response)
    {
        return response.GridOwners
            .Where(go => go?.Facilities is { Count: > 0 })
            .SelectMany(go => go.Facilities)
            .ToList();
    }

    /// <summary>
    /// Get all measurement points across all lines, including retired ones
    /// (those with a non-null <see cref="MeasurementPointDto.UnregisteredTimestamp"/>).
    /// </summary>
    /// <param name="response"></param>
    /// <returns></returns>
    public static IReadOnlyList<MeasurementPointDto> AllMeasurementPoints(this AssetsResponse response)
    {
        return response.GridOwners
            .Where(go => go?.Facilities is { Count: > 0 })
            .SelectMany(go => go.Facilities)
            .Where(facility => facility?.Line?.Spans is { Count: > 0 })
            .SelectMany(facility => facility.Line!.Spans)
            .SelectMany(span => span.SpanPhases)
            .SelectMany(phase => phase.MeasurementPoints)
            .ToList();
    }

    /// <summary>
    /// Get the lines that have at least one active measurement point, with their facility and active measurement points.
    /// A measurement point is active while its <see cref="MeasurementPointDto.UnregisteredTimestamp"/> is null or in the future.
    /// Lines with no measurement points, or only retired ones, are left out: data endpoints return 404 or no data for them.
    /// </summary>
    /// <example>
    /// <code>
    /// foreach (var instrumented in assets.InstrumentedLines())
    /// {
    ///     var current = await client.GetLatestCurrentAsync(instrumented.Line.Id);
    /// }
    /// </code>
    /// </example>
    /// <param name="response">The assets response, e.g. from <see cref="IHeimdallApiClient.GetAssetsAsync"/>.</param>
    /// <returns>The instrumented lines, in the order they appear in <paramref name="response"/>.</returns>
    public static IReadOnlyList<InstrumentedLine> InstrumentedLines(this AssetsResponse response)
    {
        var now = DateTimeOffset.UtcNow;
        return response.AllFacilities()
            .Where(facility => facility?.Line != null)
            .Select(facility => new InstrumentedLine(
                facility,
                facility.Line!,
                (facility.Line!.Spans ?? [])
                    .SelectMany(span => span.SpanPhases ?? [])
                    .SelectMany(phase => phase.MeasurementPoints ?? [])
                    .Where(mp => mp.UnregisteredTimestamp is null || mp.UnregisteredTimestamp > now)
                    .ToList()))
            .Where(instrumented => instrumented.ActiveMeasurementPoints.Count > 0)
            .ToList();
    }
}
