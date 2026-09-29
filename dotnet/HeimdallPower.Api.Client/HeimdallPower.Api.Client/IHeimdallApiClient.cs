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
/// <b>Retry behaviour:</b> The core package does <b>not</b> retry automatically.
/// Transient gateway errors (502, 503, 504) and network failures are thrown immediately
/// as <see cref="HeimdallApiException"/> or <see cref="System.Net.Http.HttpRequestException"/>.
/// For built-in retry, circuit breaking, and backoff, register the client via
/// <c>AddHeimdallPowerApiClient</c> from the <c>HeimdallPower.Api.Client.Extensions</c> package.
/// </para>
/// <para>
/// <b>Cancellation:</b> All methods accept an optional <see cref="CancellationToken"/>.
/// Cancellation is respected during the HTTP request.
/// Passing a cancelled token causes an <see cref="OperationCanceledException"/> to be thrown immediately.
/// </para>
/// <para>
/// <b>Timeouts:</b> Configure a per-request timeout by passing a pre-configured
/// <see cref="System.Net.Http.HttpClient"/> with <c>HttpClient.Timeout</c> set via
/// <see cref="HeimdallApiClientSettings.HttpClient"/>, or by
/// linking a <see cref="CancellationTokenSource"/> with a timeout to the
/// <c>cancellationToken</c> argument on each call.
/// </para>
/// <para>
/// <b>Exceptions:</b> All methods throw <see cref="HeimdallApiException"/> on non-success
/// HTTP errors (e.g. 400, 403, 404, 500, 502).
/// The <see cref="HeimdallApiException.StatusCode"/> property carries the HTTP status code.
/// A <see cref="System.UnauthorizedAccessException"/> is thrown when authentication fails
/// after a token-refresh attempt.
/// </para>
/// <para>
/// <b>Optional parameters:</b> Each data method takes a method-specific options record (e.g.
/// <see cref="GetLatestCurrentOptions"/>). New optional API parameters are added as properties on
/// these records in minor versions.
/// </para>
/// <para>
/// <b>Versioning:</b> This interface is intended for consumption and mocking. New methods may be
/// added in minor versions, so hand-written implementations may need updating when you upgrade.
/// </para>
/// </remarks>
public interface IHeimdallApiClient
{
    /// <summary>Get all assets.</summary>
    /// <returns>The full asset hierarchy including grid owners, facilities, and lines.</returns>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<AssetsResponse> GetAssetsAsync(CancellationToken cancellationToken = default);

    /// <summary>Get a list of all lines associated with the grid owner.</summary>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<IReadOnlyList<LineDto>> GetLinesAsync(CancellationToken cancellationToken = default);

    /// <summary>Get a list of facilities associated with the grid owner.</summary>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<IReadOnlyList<FacilityDto>> GetFacilitiesAsync(CancellationToken cancellationToken = default);

    /// <summary>Get the most recent current for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest current.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestCurrentOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestCurrentResponse> GetLatestCurrentAsync(Guid lineId, GetLatestCurrentOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent conductor temperature for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest conductor temperature.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestConductorTemperatureOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestConductorTemperatureResponse> GetLatestConductorTemperatureAsync(Guid lineId, GetLatestConductorTemperatureOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent icing measurements for the line, including maximum values and per-span/phase metrics.</summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest icing measurements.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestIcingOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestIcingResponse> GetLatestIcingAsync(Guid lineId, GetLatestIcingOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent sag and clearance data for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest sag and clearance measurements.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestSagAndClearanceOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestLineSagAndClearanceResponse> GetLatestSagAndClearanceAsync(Guid lineId, GetLatestSagAndClearanceOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>
    /// Get sag and clearance data for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetSagAndClearancesOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LineSagAndClearancesResponse> GetSagAndClearancesAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetSagAndClearancesOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>
    /// Get icing data for the line within a time range, including maximum values and per-span/phase metrics.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetIcingsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LineIcingsResponse> GetIcingsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetIcingsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>
    /// Get icing forecasts for the line. Covers 72 hours in 30-minute intervals.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve icing forecasts.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetIcingForecastOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<IcingForecastResponse> GetIcingForecastAsync(Guid lineId, GetIcingForecastOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent apparent power measurement for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest apparent power.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestApparentPowerOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestApparentPowerResponse> GetLatestApparentPowerAsync(Guid lineId, GetLatestApparentPowerOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get apparent power values for the line within a time range. The period between from and to must not exceed 30 days.</summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetApparentPowersOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<ApparentPowersResponse> GetApparentPowersAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetApparentPowersOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>
    /// Get currents for the line within a time range.
    /// Current is defined as the maximum current, in amperes, measured on the line at a given timestamp.
    /// The current is aggregated across the entire line using a 5-minute sliding window, where the maximum value is calculated for each window.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetCurrentsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<CurrentsResponse> GetCurrentsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetCurrentsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>
    /// Get conductor temperatures for the line within a time range.
    /// Conductor temperature is defined as the maximum and minimum temperature measured on the line at a given timestamp.
    /// The conductor temperature is aggregated across the entire line using a 5-minute sliding window, where the maximum and minimum values are calculated for each window.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetConductorTemperaturesOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<ConductorTemperaturesResponse> GetConductorTemperaturesAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetConductorTemperaturesOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent Heimdall Dynamic Line Rating (DLR) for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall DLR.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestHeimdallDlrOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestHeimdallDlrResponse> GetLatestHeimdallDlrAsync(Guid lineId, GetLatestHeimdallDlrOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent Heimdall Ambient-Adjusted Rating (AAR) for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall AAR.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestHeimdallAarOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestHeimdallAarResponse> GetLatestHeimdallAarAsync(Guid lineId, GetLatestHeimdallAarOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>
    /// Get the most recent line transient rating for the line: the short-duration overload ampacity the line can
    /// sustain for each calculated duration. Returns one timestamp and one value per calculated duration.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest line transient rating.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestLineTransientRatingOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestLineTransientRatingResponse> GetLatestLineTransientRatingAsync(Guid lineId, GetLatestLineTransientRatingOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent Heimdall Dynamic Line Rating (DLR) forecasts for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall DLR forecasts.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetHeimdallDlrForecastsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallDlrForecastResponse> GetHeimdallDlrForecastsAsync(Guid lineId, GetHeimdallDlrForecastsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.</summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall AAR forecasts.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetHeimdallAarForecastsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallAarForecastResponse> GetHeimdallAarForecastsAsync(Guid lineId, GetHeimdallAarForecastsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get Heimdall Dynamic Line Rating (DLR) values for the line within a time range. The period between from and to must not exceed 30 days.</summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetHeimdallDlrsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallDlrsResponse> GetHeimdallDlrsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetHeimdallDlrsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get Heimdall Ambient-Adjusted Rating (AAR) values for the line within a time range. The period between from and to must not exceed 30 days.</summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetHeimdallAarsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<HeimdallAarsResponse> GetHeimdallAarsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetHeimdallAarsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent circuit rating forecasts for a specified facility.</summary>
    /// <param name="facilityId">Id of the facility for which to retrieve circuit rating forecasts.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetCircuitRatingForecastsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<CircuitRatingForecastResponse> GetCircuitRatingForecastsAsync(Guid facilityId, GetCircuitRatingForecastsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get the most recent circuit rating for a specified facility.</summary>
    /// <param name="facilityId">Id of the facility for which to retrieve the latest circuit rating.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestCircuitRatingOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestCircuitRatingResponse> GetLatestCircuitRatingAsync(Guid facilityId, GetLatestCircuitRatingOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>Get circuit ratings for a specified facility within a time range. The period between from and to must not exceed 30 days.</summary>
    /// <param name="facilityId">Id of the facility.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="options">Optional query parameters, see <see cref="GetCircuitRatingsOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<CircuitRatingsResponse> GetCircuitRatingsAsync(Guid facilityId, DateTimeOffset from, DateTimeOffset to, GetCircuitRatingsOptions? options = null, CancellationToken cancellationToken = default);

    /// <summary>
    /// Get the most recent circuit transient rating for a specified facility, including the limiting facility component
    /// for each duration. Returns one timestamp and one value per calculated duration.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve the latest circuit transient rating.</param>
    /// <param name="options">Optional query parameters, see <see cref="GetLatestCircuitTransientRatingOptions"/>. Defaults apply when null.</param>
    /// <param name="cancellationToken">Token to cancel the request.</param>
    /// <exception cref="HeimdallApiException">Thrown on non-transient API errors.</exception>
    Task<LatestCircuitTransientRatingResponse> GetLatestCircuitTransientRatingAsync(Guid facilityId, GetLatestCircuitTransientRatingOptions? options = null, CancellationToken cancellationToken = default);
}
