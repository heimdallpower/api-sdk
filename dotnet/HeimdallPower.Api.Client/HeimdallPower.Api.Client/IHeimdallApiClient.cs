using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;
using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client;

/// <summary>
/// Interface for consuming the Heimdall Power API.
/// </summary>
public interface IHeimdallApiClient
{
    /// <summary>
    /// Get all assets.
    /// </summary>
    /// <returns>The full asset hierarchy including grid owners, facilities, and lines.</returns>
    Task<AssetsResponse> GetAssetsAsync();

    /// <summary>
    /// Get a list of all lines associated with the grid owner.
    /// </summary>
    Task<List<LineDto?>> GetLinesAsync();

    /// <summary>
    /// Get a list of facilities associated with the grid owner.
    /// </summary>
    Task<List<FacilityDto>> GetFacilitiesAsync();

    /// <summary>
    /// Get the most recent current for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest current.</param>
    Task<LatestCurrentResponse> GetLatestCurrentAsync(Guid lineId);

    /// <summary>
    /// Get the most recent conductor temperature for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest conductor temperature.</param>
    /// <param name="unitSystem">The unit system for response values. "metric" gives values in Celsius (C), while "imperial" gives values in Fahrenheit (F). Defaults to metric if not specified.</param>
    Task<LatestConductorTemperatureResponse> GetLatestConductorTemperatureAsync(Guid lineId, string unitSystem = "metric");

    /// <summary>
    /// Get the most recent icing measurements for the line, including maximum values and per-span/phase metrics.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest icing measurements.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="since">Optional cutoff time (UTC). Only measurements at or after this instant are considered. Older data for a span phase is excluded. If omitted, defaults to 30 min ago.</param>
    Task<LatestIcingResponse> GetLatestIcingAsync(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null);

    /// <summary>
    /// Get the most recent sag and clearance data for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest sag and clearance measurements.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="since">Optional cutoff time (UTC). Only measurements at or after this instant are considered. Older data for a span phase is excluded. If omitted, defaults to 30 min ago.</param>
    Task<LatestLineSagAndClearanceResponse> GetLatestSagAndClearanceAsync(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null);

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall DLR.</param>
    Task<LatestHeimdallDlrResponse> GetLatestHeimdallDlrAsync(Guid lineId);

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall AAR.</param>
    Task<LatestHeimdallAarResponse> GetLatestHeimdallAarAsync(Guid lineId);

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) forecasts for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall DLR forecasts.</param>
    Task<HeimdallDlrForecastResponse> GetHeimdallDlrForecastsAsync(Guid lineId);

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall AAR forecasts.</param>
    Task<HeimdallAarForecastResponse> GetHeimdallAarForecastsAsync(Guid lineId);

    /// <summary>
    /// Get the most recent circuit rating forecasts for a specified facility.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve circuit rating forecasts.</param>
    Task<CircuitRatingForecastResponse> GetCircuitRatingForecastsAsync(Guid facilityId);

    /// <summary>
    /// Get the most recent circuit rating for a specified facility.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve the latest circuit rating.</param>
    Task<LatestCircuitRatingResponse> GetLatestCircuitRatingAsync(Guid facilityId);
}
