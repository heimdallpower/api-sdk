using HeimdallPower.Api.Client.Assets;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;
using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client;

/// <summary>
/// A client that lets you consume the Heimdall Power API.
/// Throws <see cref="HeimdallApiException"/> on errors.
/// </summary>
public class HeimdallApiClient(string clientId, string clientSecret, HttpClient? httpClient = null)
{
    private readonly HeimdallApiHttpClient _heimdallApiClient = new(clientId, clientSecret, httpClient);

    /// <summary>
    /// Get all assets.
    /// </summary>
    /// <returns>The full asset hierarchy including grid owners, facilities, and lines.</returns>
    public async Task<AssetsResponse> GetAssetsAsync()
    {
        var url = UrlBuilder.BuildAssetsUrl();
        var response = await _heimdallApiClient.GetAsync<ApiResponse<AssetsResponse>>(url);
        return response.Data;
    }

    /// <summary>
    /// Get a list of all lines associated with the grid owner.
    /// </summary>
    public async Task<List<LineDto?>> GetLinesAsync()
    {
        var url = UrlBuilder.BuildAssetsUrl();
        var response = await _heimdallApiClient.GetAsync<ApiResponse<AssetsResponse>>(url);
        return response.Data.AllLines();
    }

    /// <summary>
    /// Get a list of facilities associated with the grid owner.
    /// </summary>
    public async Task<List<FacilityDto>> GetFacilitiesAsync()
    {
        var url = UrlBuilder.BuildAssetsUrl();
        var response = await _heimdallApiClient.GetAsync<ApiResponse<AssetsResponse>>(url);

        return response.Data.AllFacilities();
    }

    /// <summary>
    /// Get the most recent current for the line.
    /// Current is defined as the maximum current, in amperes, measured on the line at a given timestamp.
    /// The current is aggregated across the entire line using a 5-minute sliding window, where the maximum value is calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest current.</param>
    public async Task<LatestCurrentResponse> GetLatestCurrentAsync(Guid lineId)
    {
        var url = UrlBuilder.BuildLatestCurrentsUrl(lineId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestCurrentResponse>>(url);

        return response.Data;
    }

    /// <summary>
    /// Get the most recent conductor temperature for the line.
    /// Conductor temperature is defined as the maximum and minimum temperature measured on the line at a given timestamp.
    /// The conductor temperature is aggregated across the entire line using a 5-minute sliding window, where the maximum and minimum values are calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest conductor temperature.</param>
    /// <param name="unitSystem">The unit system for response values. "metric" gives values in Celsius (C), while "imperial" gives values in Fahrenheit (F). Defaults to metric if not specified.</param>
    public async Task<LatestConductorTemperatureResponse> GetLatestConductorTemperatureAsync(Guid lineId, string unitSystem = "metric")
    {
        var url = UrlBuilder.BuildLatestConductorTemperatureUrl(lineId, unitSystem);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestConductorTemperatureResponse>>(url);
        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) for the line.
    /// Heimdall DLR is calculated according to our own proprietary method, based on the CIGRE TB-601 standard for thermal calculation for OHLs.
    /// This method also takes the conductor temperature and current into account and uses these to adjust the weather parameters during calculations.
    /// Heimdall DLR is aggregated over the entire line. Using a 5-minute sliding window, the minimum ampacity is calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall DLR.</param>
    public async Task<LatestHeimdallDlrResponse> GetLatestHeimdallDlrAsync(Guid lineId)
    {
        var url = UrlBuilder.BuildHeimdallDlrUrl(lineId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestHeimdallDlrResponse>>(url);

        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) for the line.
    /// Heimdall AAR is calculated according to the CIGRE TB-601 standard for thermal calculation for OHLs. It is purely based on weather data from weather service providers.
    /// In this method for rating, both wind speed, wind direction, and solar heating are set to static values chosen by the customer. Therefore, only the Ambient temperature will vary dynamically.
    /// Heimdall AAR is aggregated over the entire line. Using a 5-minute sliding window, the minimum ampacity is calculated for each window.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve the latest Heimdall AAR.</param>
    public async Task<LatestHeimdallAarResponse> GetLatestHeimdallAarAsync(Guid lineId)
    {
        var url = UrlBuilder.BuildHeimdallAarUrl(lineId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestHeimdallAarResponse>>(url);

        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Dynamic Line Rating (DLR) forecasts for the line.
    /// The forecasted hours returned by the endpoint are set to 72 hours, and are provided in 1-hour intervals.
    /// The response contains a series of buckets, each with a timestamp and predictions based on different values of confidence levels p80, p90, p95 and p99.
    /// For each unique timestamp and confidence level, we pick the value from the span which has the lowest ampacity value as this will be the dimensioning value for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall DLR forecasts.</param>
    public async Task<HeimdallDlrForecastResponse> GetHeimdallDlrForecastsAsync(Guid lineId)
    {
        var url = UrlBuilder.BuildDlrForecastUrl(lineId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<HeimdallDlrForecastResponse>>(url);

        return response.Data;
    }

    /// <summary>
    /// Get the most recent Heimdall Ambient-Adjusted Rating (AAR) forecasts for the line.
    /// The forecasted hours returned by the endpoint are defined by the line’s available_forecast_hours configuration, typically 72 or 240, and are provided in 1-hour intervals.
    /// The response contains a series of buckets, each with a timestamp and predictions based on different values of confidence levels p80, p90, p95 and p99.
    /// For each unique timestamp and confidence level, we pick the value from the span which has the lowest ampacity value as this will be the dimensioning value for the line.
    /// </summary>
    /// <param name="lineId">Id of the line for which to retrieve Heimdall AAR forecasts.</param>
    public async Task<HeimdallAarForecastResponse> GetHeimdallAarForecastsAsync(Guid lineId)
    {
        var url = UrlBuilder.BuildAarForecastUrl(lineId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<HeimdallAarForecastResponse>>(url);

        return response.Data;
    }

    /// <summary>
    /// Get the most recent circuit rating forecasts for a specified facility.
    /// The forecasted hours returned by the endpoint are set to 72 hours
    /// and are provided in 1-hour intervals.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve circuit rating forecasts.</param>
    public async Task<CircuitRatingForecastResponse> GetCircuitRatingForecastsAsync(Guid facilityId)
    {
        var url = UrlBuilder.BuildCircuitRatingForecastUrl(facilityId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<CircuitRatingForecastResponse>>(url);

        return response.Data;
    }

    /// <summary>
    /// Get the most recent circuit rating forecasts for a specified facility.
    /// The forecasted hours returned by the endpoint are set to 72 hours
    /// and are provided in 1-hour intervals.
    /// </summary>
    /// <param name="facilityId">Id of the facility for which to retrieve circuit rating forecasts.</param>
    public async Task<LatestCircuitRatingResponse> GetLatestCircuitRatingAsync(Guid facilityId)
    {
        var url = UrlBuilder.BuildCircuitRatingUrl(facilityId);
        var response = await _heimdallApiClient.GetAsync<ApiResponse<LatestCircuitRatingResponse>>(url);

        return response.Data;
    }
}
