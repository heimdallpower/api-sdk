using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;
using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client;

/// <summary>
/// A client that lets you consume the Heimdall Power API.
/// Throws <see cref="HeimdallApiException"/> on errors.
/// </summary>
public class HeimdallApiClient : IHeimdallApiClient
{
    private const string ApiUrl = "https://external-api.heimdallcloud.com";
    private const string Policy = "B2C_1A_CLIENTCREDENTIALSFLOW";
    private const string Instance = "https://hpadb2cprod.b2clogin.com";
    private const string Domain = "hpadb2cprod.onmicrosoft.com";
    private const string Scope = $"https://{Domain}/dc5758ae-4eea-416e-9e61-812914d9a49a/.default";
    private const string Authority = $"{Instance}/tfp/{Domain}/{Policy}";
    private readonly HeimdallApiHttpClient _heimdallApiClient;

    /// <summary>
    /// A client that lets you consume the Heimdall Power API.
    /// Throws <see cref="HeimdallApiException"/> on errors.
    /// </summary>
    public HeimdallApiClient(string clientId, string clientSecret, HttpClient? httpClient = null, Dictionary<string, string>? clientMetadata = null, HttpMessageHandler? proxyHandler = null)
    {
        var accessTokenProvider = new AccessTokenProvider(clientId, clientSecret, Authority, Scope, proxyHandler);
        _heimdallApiClient = new HeimdallApiHttpClient(accessTokenProvider, httpClient ?? new HttpClient { BaseAddress = new Uri(ApiUrl) }, clientMetadata);
    }

    /// <summary>
    /// Get all assets.
    /// </summary>
    /// <returns>The full asset hierarchy including grid owners, facilities, and lines.</returns>
    public async Task<AssetsResponse> GetAssetsAsync(CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildAssetsUrl();
        var response = await _heimdallApiClient.GetAsync<ApiResponse<AssetsResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get a list of all lines associated with the grid owner.
    /// </summary>
    public async Task<List<LineDto?>> GetLinesAsync(CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildAssetsUrl();
        var response = await _heimdallApiClient.GetAsync<ApiResponse<AssetsResponse>>(url, cancellationToken);
        return response.Data.AllLines();
    }

    /// <summary>
    /// Get a list of facilities associated with the grid owner.
    /// </summary>
    public async Task<List<FacilityDto>> GetFacilitiesAsync(CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildAssetsUrl();
        var response = await _heimdallApiClient.GetAsync<ApiResponse<AssetsResponse>>(url, cancellationToken);
        return response.Data.AllFacilities();
    }

    /// <summary>
    /// Get the most recent current for the line.
    /// Current is defined as the maximum current, in amperes, measured on the line at a given timestamp.
    /// The current is aggregated across the entire line using a 5-minute sliding window, where the maximum value is calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest current.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestCurrentResponse> GetLatestCurrentAsync(Guid lineId, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestCurrentsUrl(lineId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestCurrentResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent conductor temperature for the line.
    /// Conductor temperature is defined as the maximum and minimum temperature measured on the line at a given timestamp.
    /// The conductor temperature is aggregated across the entire line using a 5-minute sliding window, where the maximum and minimum values are calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest conductor temperature.</param>
    /// <param name="unitSystem">The unit system for response values. "metric" gives values in Celsius (C), while "imperial" gives values in Fahrenheit (F). Defaults to metric if not specified.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestConductorTemperatureResponse> GetLatestConductorTemperatureAsync(Guid lineId, string unitSystem = "metric", CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestConductorTemperatureUrl(lineId, unitSystem);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestConductorTemperatureResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent icing measurements for the line, including maximum values and per-span/phase metrics.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest icing measurements.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="since">Optional cutoff time (UTC). Only measurements at or after this instant are considered. Older data for a span phase is excluded. If omitted, defaults to 30 min ago.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestIcingResponse> GetLatestIcingAsync(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestIcingUrl(lineId, unitSystem, since);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestIcingResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent sag and clearance measurements for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest sag and clearance measurements.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="since">Optional cutoff time (UTC). Only measurements at or after this instant are considered. Older data for a span phase is excluded. If omitted, defaults to 30 min ago.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestLineSagAndClearanceResponse> GetLatestSagAndClearanceAsync(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestSagAndClearanceUrl(lineId, unitSystem, since);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestLineSagAndClearanceResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get sag and clearance data for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LineSagAndClearancesResponse> GetSagAndClearancesAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric", CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildSagAndClearanceUrl(lineId, from, to, unitSystem);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LineSagAndClearancesResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get icing data for the line within a time range, including maximum values and per-span/phase metrics.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, N, %, while "imperial" uses lb/ft, lbf, %.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LineIcingsResponse> GetIcingsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric", CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildIcingUrl(lineId, from, to, unitSystem);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LineIcingsResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get icing forecasts for the line. Covers 72 hours in 30-minute intervals.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve icing forecasts.</param>
    /// <param name="unitSystem">The unit system for the measurements. "metric" uses kg/m, "imperial" uses lb/ft. Defaults to metric.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<IcingForecastResponse> GetIcingForecastAsync(Guid lineId, string unitSystem = "metric", CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildIcingForecastUrl(lineId, unitSystem);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<IcingForecastResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent apparent power measurement for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest apparent power.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestApparentPowerResponse> GetLatestApparentPowerAsync(Guid lineId, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestApparentPowerUrl(lineId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestApparentPowerResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get apparent power values for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<ApparentPowersResponse> GetApparentPowersAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildApparentPowersUrl(lineId, from, to);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<ApparentPowersResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get currents for the line within a time range.
    /// Current is defined as the maximum current, in amperes, measured on the line at a given timestamp.
    /// The current is aggregated across the entire line using a 5-minute sliding window, where the maximum value is calculated for each window.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<CurrentsResponse> GetCurrentsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildCurrentsUrl(lineId, from, to);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<CurrentsResponse>>(url, cancellationToken);
        return response.Data;
    }

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
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<ConductorTemperaturesResponse> GetConductorTemperaturesAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric", CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildConductorTemperaturesUrl(lineId, from, to, unitSystem);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<ConductorTemperaturesResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) for the line.
    /// Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601 standard for thermal calculation for OHLs.
    /// This method also takes the conductor temperature and current into account and uses these to adjust the weather parameters during calculations.
    /// Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum ampacity is calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall DLR.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestHeimdallDlrResponse> GetLatestHeimdallDlrAsync(Guid lineId, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestHeimdallDlrUrl(lineId, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestHeimdallDlrResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) for the line.
    /// Heimdall AAR is calculated according to the CIGRE TB-601 standard for thermal calculation for OHLs. It is purely based on weather data from weather service providers.
    /// In this method for rating, both wind speed, wind direction, and solar heating are set to static values chosen by the customer. Therefore, only the Ambient temperature will vary dynamically.
    /// Heimdall AAR is aggregated over the entire line. Using a 5-minute sliding window, the minimum ampacity is calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall AAR.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestHeimdallAarResponse> GetLatestHeimdallAarAsync(Guid lineId, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestHeimdallAarUrl(lineId, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestHeimdallAarResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) forecasts for the line.
    /// The forecasted hours returned by the endpoint are set to 72 hours, and are provided in 1-hour intervals.
    /// The response contains a series of buckets, each with a timestamp and predictions based on different values of confidence levels p80, p90, p95 and p99.
    /// For each unique timestamp and confidence level, we pick the value from the span which has the lowest ampacity value as this will be the dimensioning value for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall DLR forecasts.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<HeimdallDlrForecastResponse> GetHeimdallDlrForecastsAsync(Guid lineId, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildDlrForecastUrl(lineId, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<HeimdallDlrForecastResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.
    /// The forecasted hours returned by the endpoint are defined by the line’s available_forecast_hours configuration, typically 72 or 240, and are provided in 1-hour intervals.
    /// The response contains a series of buckets, each with a timestamp and predictions based on different values of confidence levels p80, p90, p95 and p99.
    /// For each unique timestamp and confidence level, we pick the value from the span which has the lowest ampacity value as this will be the dimensioning value for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall AAR forecasts.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<HeimdallAarForecastResponse> GetHeimdallAarForecastsAsync(Guid lineId, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildAarForecastUrl(lineId, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<HeimdallAarForecastResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get Heimdall Dynamic Line Rating (DLR) values for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<HeimdallDlrsResponse> GetHeimdallDlrsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildHeimdallDlrsUrl(lineId, from, to, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<HeimdallDlrsResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get Heimdall Ambient-Adjusted Rating (AAR) values for the line within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="lineId">Id of the line.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<HeimdallAarsResponse> GetHeimdallAarsAsync(Guid lineId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildHeimdallAarsUrl(lineId, from, to, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<HeimdallAarsResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent circuit rating forecasts for a specified facility.
    /// The forecasted hours returned by the endpoint are set to 72 hours
    /// and are provided in 1-hour intervals.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve circuit rating forecasts.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<CircuitRatingForecastResponse> GetCircuitRatingForecastsAsync(Guid facilityId, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildCircuitRatingForecastUrl(facilityId, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<CircuitRatingForecastResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent circuit rating for a specified facility.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve the latest circuit rating.</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<LatestCircuitRatingResponse> GetLatestCircuitRatingAsync(Guid facilityId, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildLatestCircuitRatingUrl(facilityId, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestCircuitRatingResponse>>(url, cancellationToken);
        return response.Data;
    }

    /// <summary>
    /// Get circuit ratings for a specified facility within a time range.
    /// The period between from and to must not exceed 30 days.
    /// </summary>
    /// <param name="facilityId">Id of the facility.</param>
    /// <param name="from">Start of the time range (inclusive).</param>
    /// <param name="to">End of the time range (inclusive).</param>
    /// <param name="quantity">The quantity to return. Defaults to current (amperes). Use ApparentPower for MVA.</param>
    /// <param name="cancellationToken">Token to cancel the request and any retry delays.</param>
    public async Task<CircuitRatingsResponse> GetCircuitRatingsAsync(Guid facilityId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current, CancellationToken cancellationToken = default)
    {
        var url = UrlBuilder.BuildCircuitRatingsUrl(facilityId, from, to, quantity);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<CircuitRatingsResponse>>(url, cancellationToken);
        return response.Data;
    }
}
