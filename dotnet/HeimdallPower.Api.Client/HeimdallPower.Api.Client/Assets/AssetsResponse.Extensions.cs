namespace HeimdallPower.Api.Client.Assets;

public static class AssetsResponseExtensions
{
    /// <summary>
    /// Get all available lines
    /// </summary>
    /// <param name="response"></param>
    /// <returns></returns>
    public static List<LineDto?> AllLines(this AssetsResponse response)
    {
        return response.GridOwners
            .Where(go => go?.Facilities is { Count: > 0 })
            .SelectMany(go => go.Facilities
                .Where(facility => facility?.Line != null)
                .Select(facility => facility.Line))
            .ToList();
    }

    /// <summary>
    /// Get all available facilities
    /// </summary>
    /// <param name="response"></param>
    /// <returns></returns>
    public static List<FacilityDto> AllFacilities(this AssetsResponse response)
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
    public static List<MeasurementPointDto> AllMeasurementPoints(this AssetsResponse response)
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
}
