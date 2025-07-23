using System.Collections.Specialized;
using HeimdallPower.Api.Client.ExtensionMethods;

namespace HeimdallPower.Api.Client;

internal static class UrlBuilder
{
    //Modules
    private const string CapacityMonitoring = "capacity_monitoring";
    private const string GridInsight = "grid_insights";
    private const string Assets = "assets";

    private const string V1 = "v1";

    //Resources
    private const string Lines = "lines";
    private const string Facilities = "facilities";
    private const string AssetsResource = "assets";

    //Endpoints
    private const string CircuitRatingForecasts = "circuit_ratings/forecasts";
    private const string CircuitRatingLatest = "circuit_ratings/latest";
    private const string ConductorTemperatures = "conductor_temperatures/latest";
    private const string Currents = "currents/latest";
    private const string HeimdallDlr = "heimdall_dlrs/latest";
    private const string HeimdallAar = "heimdall_aars/latest";
    private const string HeimdallDlrForecast = "heimdall_dlrs/forecasts";
    private const string HeimdallAarForecast = "heimdall_aars/forecasts";

    public static string BuildLatestConductorTemperatureUrl(Guid lineId, string unitSystem)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("unit_system", unitSystem);

        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: ConductorTemperatures, queryParams: queryParams);
    }

    public static string BuildLatestCurrentsUrl(Guid lineId)
        => GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: Currents);

    public static string BuildHeimdallDlrUrl(Guid lineId)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallDlr);

    public static string BuildHeimdallAarUrl(Guid lineId)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallAar);

    public static string BuildDlrForecastUrl(Guid lineId)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallDlrForecast);

    public static string BuildAarForecastUrl(Guid lineId)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallAarForecast);

    public static string BuildAssetsUrl()
        => GetResourceUrl(module: Assets, apiVersion: V1, resource: AssetsResource);

    public static string BuildCircuitRatingForecastUrl(Guid facilityId)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Facilities, resourceId: facilityId.ToString(), endpoint: CircuitRatingForecasts);

    public static string BuildCircuitRatingUrl(Guid facilityId)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Facilities, resourceId: facilityId.ToString(), endpoint: CircuitRatingLatest);

    private static string GetResourceUrl(string module, string apiVersion, string resource)
        => $"{module}/{apiVersion}/{resource}";

    private static string GetFullUrl(string module, string apiVersion, string resource, string resourceId, string endpoint)
        => $"{GetResourceUrl(module, apiVersion, resource)}/{resourceId}/{endpoint}";

    private static string GetFullUrl(string module, string apiVersion, string resource, string resourceId, string endpoint, NameValueCollection queryParams)
        => $"{GetResourceUrl(module, apiVersion, resource)}/{resourceId}/{endpoint}{queryParams.ToQueryString()}";
}
