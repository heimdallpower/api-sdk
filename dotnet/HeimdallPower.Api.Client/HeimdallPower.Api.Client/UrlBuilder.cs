using System.Collections.Specialized;
using HeimdallPower.Api.Client.CapacityMonitoring;

namespace HeimdallPower.Api.Client;

internal static class UrlBuilder
{
    // Modules
    private const string CapacityMonitoring = "capacity_monitoring";
    private const string GridInsight = "grid_insights";
    private const string Assets = "assets";

    private const string V1 = "v1";

    // Resources
    private const string Lines = "lines";
    private const string Facilities = "facilities";
    private const string AssetsResource = "assets";

    // Endpoints
    private const string CircuitRatings = "circuit_ratings";
    private const string CircuitRatingForecasts = "circuit_ratings/forecasts";
    private const string CircuitRatingLatest = "circuit_ratings/latest";
    private const string ConductorTemperatures = "conductor_temperatures/latest";
    private const string ConductorTemperaturesHistorical = "conductor_temperatures";
    private const string Currents = "currents/latest";
    private const string CurrentsHistorical = "currents";
    private const string HeimdallDlrs = "heimdall_dlrs";
    private const string HeimdallDlr = "heimdall_dlrs/latest";
    private const string HeimdallAars = "heimdall_aars";
    private const string HeimdallAar = "heimdall_aars/latest";
    private const string HeimdallDlrForecast = "heimdall_dlrs/forecasts";
    private const string HeimdallAarForecast = "heimdall_aars/forecasts";
    private const string IcingLatest = "icing/latest";
    private const string IcingForecast = "icing/forecast";
    private const string ApparentPowerLatest = "apparent_power/latest";
    private const string ApparentPower = "apparent_power";
    private const string SagAndClearanceLatest = "sag_and_clearance/latest";
    private const string SagAndClearance = "sag_and_clearance";

    public static string BuildLatestConductorTemperatureUrl(Guid lineId, string unitSystem)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("unit_system", unitSystem);

        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: ConductorTemperatures, queryParams: queryParams);
    }

    public static string BuildLatestCurrentsUrl(Guid lineId)
        => GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: Currents);

    public static string BuildCurrentsUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("from_timestamp", from.ToUniversalTime().ToString("o"))
            .AddQueryParam("to_timestamp", to.ToUniversalTime().ToString("o"));
        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: CurrentsHistorical, queryParams: queryParams);
    }

    public static string BuildConductorTemperaturesUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric")
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("from_timestamp", from.ToUniversalTime().ToString("o"))
            .AddQueryParam("to_timestamp", to.ToUniversalTime().ToString("o"))
            .AddQueryParam("unit_system", unitSystem);
        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: ConductorTemperaturesHistorical, queryParams: queryParams);
    }

    public static string BuildLatestHeimdallDlrUrl(Guid lineId, Quantity quantity = Quantity.Current)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallDlr,
            queryParams: new NameValueCollection().AddQueryParam("quantity", quantity.ToQueryValue()));

    public static string BuildLatestHeimdallAarUrl(Guid lineId, Quantity quantity = Quantity.Current)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallAar,
            queryParams: new NameValueCollection().AddQueryParam("quantity", quantity.ToQueryValue()));

    public static string BuildDlrForecastUrl(Guid lineId, Quantity quantity = Quantity.Current)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallDlrForecast,
            queryParams: new NameValueCollection().AddQueryParam("quantity", quantity.ToQueryValue()));

    public static string BuildAarForecastUrl(Guid lineId, Quantity quantity = Quantity.Current)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallAarForecast,
            queryParams: new NameValueCollection().AddQueryParam("quantity", quantity.ToQueryValue()));

    public static string BuildHeimdallDlrsUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("from_timestamp", from.ToUniversalTime().ToString("o"))
            .AddQueryParam("to_timestamp", to.ToUniversalTime().ToString("o"))
            .AddQueryParam("quantity", quantity.ToQueryValue());
        return GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallDlrs, queryParams: queryParams);
    }

    public static string BuildHeimdallAarsUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("from_timestamp", from.ToUniversalTime().ToString("o"))
            .AddQueryParam("to_timestamp", to.ToUniversalTime().ToString("o"))
            .AddQueryParam("quantity", quantity.ToQueryValue());
        return GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: HeimdallAars, queryParams: queryParams);
    }

    public static string BuildAssetsUrl()
        => GetResourceUrl(module: Assets, apiVersion: V1, resource: AssetsResource);

    public static string BuildCircuitRatingForecastUrl(Guid facilityId, Quantity quantity = Quantity.Current)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Facilities, resourceId: facilityId.ToString(), endpoint: CircuitRatingForecasts,
            queryParams: new NameValueCollection().AddQueryParam("quantity", quantity.ToQueryValue()));

    public static string BuildLatestCircuitRatingUrl(Guid facilityId, Quantity quantity = Quantity.Current)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Facilities, resourceId: facilityId.ToString(), endpoint: CircuitRatingLatest,
            queryParams: new NameValueCollection().AddQueryParam("quantity", quantity.ToQueryValue()));

    public static string BuildCircuitRatingsUrl(Guid facilityId, DateTimeOffset from, DateTimeOffset to, Quantity quantity = Quantity.Current)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("from_timestamp", from.ToUniversalTime().ToString("o"))
            .AddQueryParam("to_timestamp", to.ToUniversalTime().ToString("o"))
            .AddQueryParam("quantity", quantity.ToQueryValue());
        return GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Facilities, resourceId: facilityId.ToString(), endpoint: CircuitRatings, queryParams: queryParams);
    }

    public static string BuildLatestIcingUrl(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("unit_system", unitSystem);

        if (since.HasValue)
            queryParams.AddQueryParam("since", since.Value.ToUniversalTime().ToString("o"));

        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: IcingLatest, queryParams: queryParams);
    }

    public static string BuildIcingForecastUrl(Guid lineId, string unitSystem = "metric")
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("unit_system", unitSystem);
        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: IcingForecast, queryParams: queryParams);
    }

    public static string BuildLatestApparentPowerUrl(Guid lineId)
        => GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: ApparentPowerLatest);

    public static string BuildApparentPowersUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("from_timestamp", from.ToUniversalTime().ToString("o"))
            .AddQueryParam("to_timestamp", to.ToUniversalTime().ToString("o"));
        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: ApparentPower, queryParams: queryParams);
    }

    public static string BuildLatestSagAndClearanceUrl(Guid lineId, string unitSystem = "metric", DateTimeOffset? since = null)
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("unit_system", unitSystem);

        if (since.HasValue)
            queryParams.AddQueryParam("since", since.Value.ToUniversalTime().ToString("o"));

        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: SagAndClearanceLatest, queryParams: queryParams);
    }

    public static string BuildSagAndClearanceUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, string unitSystem = "metric")
    {
        var queryParams = new NameValueCollection()
            .AddQueryParam("from_timestamp", from.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffffffZ"))
            .AddQueryParam("to_timestamp", to.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss.fffffffZ"))
            .AddQueryParam("unit_system", unitSystem);
        return GetFullUrl(module: GridInsight, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: SagAndClearance, queryParams: queryParams);
    }

    private static string GetResourceUrl(string module, string apiVersion, string resource)
        => $"{module}/{apiVersion}/{resource}";

    private static string GetFullUrl(string module, string apiVersion, string resource, string resourceId, string endpoint)
        => $"{GetResourceUrl(module, apiVersion, resource)}/{resourceId}/{endpoint}";

    private static string GetFullUrl(string module, string apiVersion, string resource, string resourceId, string endpoint, NameValueCollection queryParams)
        => $"{GetResourceUrl(module, apiVersion, resource)}/{resourceId}/{endpoint}{queryParams.ToQueryString()}";
}
