namespace HeimdallPower.Api.Client.Assets;

/// <summary>
/// A line with at least one active measurement point, together with its facility.
/// Returned by <see cref="HeimdallApiClientAssetsExtensions.GetInstrumentedLinesAsync"/> and
/// <see cref="AssetsResponseExtensions.InstrumentedLines"/>.
/// </summary>
/// <param name="Facility">The facility the line belongs to. Use its id for facility endpoints such as circuit ratings.</param>
/// <param name="Line">The line. Use its id for line endpoints such as currents and DLR.</param>
/// <param name="ActiveMeasurementPoints">
/// The line's active measurement points across all spans and span phases: those whose
/// <see cref="MeasurementPointDto.UnregisteredTimestamp"/> is null or in the future. Never empty.
/// </param>
public sealed record InstrumentedLine(
    FacilityDto Facility,
    LineDto Line,
    IReadOnlyList<MeasurementPointDto> ActiveMeasurementPoints);
