using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;
using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client;

/// <summary>
/// Interface for consuming the Heimdall Power API.
/// </summary>
/// <remarks>
/// <para>
/// <b>Retry behavior:</b> All methods automatically retry up to 3 times with exponential
/// backoff (1 s → 2 s → 4 s) when the server or Application Gateway returns a transient
/// error: <c>502 Bad Gateway</c>, <c>503 Service Unavailable</c>, or
/// <c>504 Gateway Timeout</c>. Network-level failures (<see cref="System.Net.Http.HttpRequestException"/>)
/// are retried on the same schedule.
/// If all 3 retry attempts are exhausted, a <see cref="HeimdallApiException"/> is thrown
/// with the status code of the last failed response.
/// </para>
/// <para>
/// <b>Exceptions:</b> All methods throw <see cref="HeimdallApiException"/> on non-transient
/// HTTP errors (e.g. 400, 403, 404, 500) or after all retries are exhausted on transient errors.
/// The <see cref="HeimdallApiException.StatusCode"/> property carries the HTTP status code.
/// A <see cref="System.UnauthorizedAccessException"/> is thrown when authentication fails
/// after a token-refresh attempt.
/// </para>
/// </remarks>
public interface IHeimdallApiClient
{
    /// <summary>
    /// Get all assets.
    /// </summary>
    /// <returns>The full asset hierarchy including grid owners, facilities, and lines.</returns>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<AssetsResponse> GetAssetsAsync();

    /// <summary>
    /// Get a list of all lines associated with the grid owner.
    /// </summary>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<List<LineDto?>> GetLinesAsync();

    /// <summary>
    /// Get a list of facilities associated with the grid owner.
    /// </summary>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<List<FacilityDto>> GetFacilitiesAsync();

    /// <summary>
    /// Get the most recent current for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest current.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestCurrentResponse> GetLatestCurrentAsync(Guid lineId);

    /// <summary>
    /// Get the most recent conductor temperature for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest conductor temperature.</param>
    /// <param name="unitSystem">The unit system for response values. "metric" gives values in Celsius (C), while "imperial" gives values in Fahrenheit (F). Defaults to metric if not specified.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestConductorTemperatureResponse> GetLatestConductorTemperatureAsync(Guid lineId, string unitSystem = "metric");

    /// <summary>
    /// Get the most recent icing measurements for the line, including maximum values and per-span/phase metrics.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest icing measurements.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="since">Optional cutoff time (UTC). Only measurements at or after this instant are considered. Older data for a span phase is excluded. If omitted, defaults to 30 min ago.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestIcingResponse> GetLatestIcingAsync(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null);

    /// <summary>
    /// Get the most recent sag and clearance data for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest sag and clearance measurements.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="since">Optional cutoff time (UTC). Only measurements at or after this instant are considered. Older data for a span phase is excluded. If omitted, defaults to 30 min ago.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestLineSagAndClearanceResponse> GetLatestSagAndClearanceAsync(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null);

    /// <summary>
    /// Get sag and clearance data for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    Task<LineSagAndClearancesResponse> GetSagAndClearancesAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric");

    /// <summary>
    /// Get icing data for the line within a time range, including maximum values and per-span/phase metrics.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    Task<LineIcingsResponse> GetIcingsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric");

    /// <summary>
    /// Get icing forecasts for the line. Covers 72 hours in 30-minute intervals.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve icing forecasts.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, "imperial" uses lb/ft. Defaults to metric.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<IcingForecastResponse> GetIcingForecastAsync(Guid lineId, string unitSystem = "metric");

    /// <summary>
    /// Get the most recent apparent power measurement for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest apparent power.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestApparentPowerResponse> GetLatestApparentPowerAsync(Guid lineId);

    /// <summary>
    /// Get apparent power values for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<ApparentPowersResponse> GetApparentPowersAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to);

    /// <summary>
    /// Get currents for the line within a time range.
    /// Current is defined as the maximum current, in amperes, measured on the line at a given timestamp.
    /// The current is aggregated across the entire line using a 5-minute sliding window, where the maximum value is calculated for each window.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<CurrentsResponse> GetCurrentsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to);

    /// <summary>
    /// Get conductor temperatures for the line within a time range.
    /// Conductor temperature is defined as the maximum and minimum temperature measured on the line at a given timestamp.
    /// The conductor temperature is aggregated across the entire line using a 5-minute sliding window, where the maximum and minimum values are calculated for each window.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="unitSystem">The unit system for response values. "metric" gives values in Celsius (C), while "imperial" gives values in Fahrenheit (F). Defaults to metric if not specified.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<ConductorTemperaturesResponse> GetConductorTemperaturesAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric");

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall DLR.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestHeimdallDlrResponse> GetLatestHeimdallDlrAsync(Guid lineId, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall AAR.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestHeimdallAarResponse> GetLatestHeimdallAarAsync(Guid lineId, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) forecasts for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall DLR forecasts.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallDlrForecastResponse> GetHeimdallDlrForecastsAsync(Guid lineId, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall AAR forecasts.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallAarForecastResponse> GetHeimdallAarForecastsAsync(Guid lineId, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get Heimdall Dynamic Line Rating (DLR) values for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallDlrsResponse> GetHeimdallDlrsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get Heimdall Ambient-Adjusted Rating (AAR) values for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallAarsResponse> GetHeimdallAarsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get the most recent circuit rating forecasts for a specified facility.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve circuit rating forecasts.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<CircuitRatingForecastResponse> GetCircuitRatingForecastsAsync(Guid facilityId, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get the most recent circuit rating for a specified facility.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve the latest circuit rating.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestCircuitRatingResponse> GetLatestCircuitRatingAsync(Guid facilityId, Quantity quantity = Quantity.Current);

    /// <summary>
    /// Get circuit ratings for a specified facility within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="facilityId">Id of the facility.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<CircuitRatingsResponse> GetCircuitRatingsAsync(Guid facilityId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current);
}
