using System.Collections.Specialized;
using System.Globalization;
using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.CapacityMonitoring.Facilities;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines;
using HeimdallPower.Api.Client.CapacityMonitoring.Lines.Forecasts;
using HeimdallPower.Api.Client.GridInsights.Lines;

namespace HeimdallPower.Api.Client;

/// <summary>
/// Builds request URLs. Each builder takes the public options record of its endpoint, so the records are the
/// single source of defaults and a new option only needs a property plus one line here.
/// </summary>
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
    private const string CircuitTransientRatingLatest = "circuit_transient_ratings/latest";
    private const string LineTransientRatingLatest = "transient_ratings/latest";
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
    private const string Icing = "icing";
    private const string ApparentPowerLatest = "apparent_power/latest";
    private const string ApparentPower = "apparent_power";
    private const string SagAndClearanceLatest = "sag_and_clearance/latest";
    private const string SagAndClearance = "sag_and_clearance";

    public static string BuildAssetsUrl()
        => GetResourceUrl(module: Assets, apiVersion: V1, resource: AssetsResource);

    // Grid insights

    public static string BuildLatestCurrentsUrl(Guid lineId, GetLatestCurrentOptions options)
        => LineUrl(GridInsight, lineId, Currents, Query().AddSince(options.Since).AddInclude(options.Include?.ToQueryValue()));

    public static string BuildCurrentsUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetCurrentsOptions options)
        => LineUrl(GridInsight, lineId, CurrentsHistorical, Query(from, to).AddInclude(options.Include?.ToQueryValue()));

    public static string BuildLatestConductorTemperatureUrl(Guid lineId, GetLatestConductorTemperatureOptions options)
        => LineUrl(GridInsight, lineId, ConductorTemperatures,
            Query().AddUnitSystem(options.UnitSystem).AddSince(options.Since).AddInclude(options.Include?.ToQueryValue()));

    public static string BuildConductorTemperaturesUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetConductorTemperaturesOptions options)
        => LineUrl(GridInsight, lineId, ConductorTemperaturesHistorical,
            Query(from, to).AddUnitSystem(options.UnitSystem).AddInclude(options.Include?.ToQueryValue()));

    public static string BuildLatestIcingUrl(Guid lineId, GetLatestIcingOptions options)
        => LineUrl(GridInsight, lineId, IcingLatest, Query().AddUnitSystem(options.UnitSystem).AddSince(options.Since));

    public static string BuildIcingUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetIcingsOptions options)
        => LineUrl(GridInsight, lineId, Icing, Query(from, to).AddUnitSystem(options.UnitSystem));

    public static string BuildIcingForecastUrl(Guid lineId, GetIcingForecastOptions options)
        => LineUrl(GridInsight, lineId, IcingForecast, Query().AddUnitSystem(options.UnitSystem));

    public static string BuildLatestSagAndClearanceUrl(Guid lineId, GetLatestSagAndClearanceOptions options)
        => LineUrl(GridInsight, lineId, SagAndClearanceLatest, Query().AddUnitSystem(options.UnitSystem).AddSince(options.Since));

    public static string BuildSagAndClearanceUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetSagAndClearancesOptions options)
        => LineUrl(GridInsight, lineId, SagAndClearance, Query(from, to).AddUnitSystem(options.UnitSystem));

    public static string BuildLatestApparentPowerUrl(Guid lineId, GetLatestApparentPowerOptions options)
        => LineUrl(GridInsight, lineId, ApparentPowerLatest, Query().AddSince(options.Since));

    // GetApparentPowersOptions has no properties yet; it is taken here so a future one is wired in the same place.
    public static string BuildApparentPowersUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetApparentPowersOptions options)
        => LineUrl(GridInsight, lineId, ApparentPower, Query(from, to));

    // Capacity monitoring: lines

    public static string BuildLatestHeimdallDlrUrl(Guid lineId, GetLatestHeimdallDlrOptions options)
        => LineUrl(CapacityMonitoring, lineId, HeimdallDlr, Query().AddQuantity(options.Quantity).AddSince(options.Since).AddInclude(options.Include?.ToQueryValue()));

    public static string BuildLatestHeimdallAarUrl(Guid lineId, GetLatestHeimdallAarOptions options)
        => LineUrl(CapacityMonitoring, lineId, HeimdallAar, Query().AddQuantity(options.Quantity).AddSince(options.Since));

    public static string BuildLatestLineTransientRatingUrl(Guid lineId, GetLatestLineTransientRatingOptions options)
        => LineUrl(CapacityMonitoring, lineId, LineTransientRatingLatest, Query().AddQuantity(options.Quantity).AddSince(options.Since));

    public static string BuildDlrForecastUrl(Guid lineId, GetHeimdallDlrForecastsOptions options)
        => LineUrl(CapacityMonitoring, lineId, HeimdallDlrForecast, Query().AddQuantity(options.Quantity));

    public static string BuildAarForecastUrl(Guid lineId, GetHeimdallAarForecastsOptions options)
        => LineUrl(CapacityMonitoring, lineId, HeimdallAarForecast, Query().AddQuantity(options.Quantity));

    public static string BuildHeimdallDlrsUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetHeimdallDlrsOptions options)
        => LineUrl(CapacityMonitoring, lineId, HeimdallDlrs, Query(from, to).AddQuantity(options.Quantity).AddInclude(options.Include?.ToQueryValue()));

    public static string BuildHeimdallAarsUrl(Guid lineId, DateTimeOffset from, DateTimeOffset to, GetHeimdallAarsOptions options)
        => LineUrl(CapacityMonitoring, lineId, HeimdallAars, Query(from, to).AddQuantity(options.Quantity));

    // Capacity monitoring: facilities

    public static string BuildCircuitRatingForecastUrl(Guid facilityId, GetCircuitRatingForecastsOptions options)
        => FacilityUrl(facilityId, CircuitRatingForecasts, Query().AddQuantity(options.Quantity));

    public static string BuildLatestCircuitRatingUrl(Guid facilityId, GetLatestCircuitRatingOptions options)
        => FacilityUrl(facilityId, CircuitRatingLatest, Query().AddQuantity(options.Quantity).AddSince(options.Since));

    public static string BuildCircuitRatingsUrl(Guid facilityId, DateTimeOffset from, DateTimeOffset to, GetCircuitRatingsOptions options)
        => FacilityUrl(facilityId, CircuitRatings, Query(from, to).AddQuantity(options.Quantity));

    public static string BuildLatestCircuitTransientRatingUrl(Guid facilityId, GetLatestCircuitTransientRatingOptions options)
        => FacilityUrl(facilityId, CircuitTransientRatingLatest, Query().AddQuantity(options.Quantity).AddSince(options.Since));

    // Query helpers

    private static NameValueCollection Query() => new();

    private static NameValueCollection Query(DateTimeOffset from, DateTimeOffset to)
        => new NameValueCollection()
            .AddQueryParam("from_timestamp", ToApiTimestamp(from))
            .AddQueryParam("to_timestamp", ToApiTimestamp(to));

    private static NameValueCollection AddSince(this NameValueCollection queryParams, DateTimeOffset? since)
        => since.HasValue ? queryParams.AddQueryParam("since", ToApiTimestamp(since.Value)) : queryParams;

    private static NameValueCollection AddInclude(this NameValueCollection queryParams, string? include)
        => include is null ? queryParams : queryParams.AddQueryParam("include", include);

    private static NameValueCollection AddUnitSystem(this NameValueCollection queryParams, UnitSystem unitSystem)
        => queryParams.AddQueryParam("unit_system", unitSystem.ToQueryValue());

    private static NameValueCollection AddQuantity(this NameValueCollection queryParams, Quantity quantity)
        => queryParams.AddQueryParam("quantity", quantity.ToQueryValue());

    private static string ToApiTimestamp(DateTimeOffset timestamp)
        => timestamp.ToUniversalTime().ToString("yyyy-MM-dd'T'HH:mm:ss.fffffff'Z'", CultureInfo.InvariantCulture);

    // URL composition

    private static string LineUrl(string module, Guid lineId, string endpoint, NameValueCollection queryParams)
        => GetFullUrl(module: module, apiVersion: V1, resource: Lines, resourceId: lineId.ToString(), endpoint: endpoint, queryParams: queryParams);

    private static string FacilityUrl(Guid facilityId, string endpoint, NameValueCollection queryParams)
        => GetFullUrl(module: CapacityMonitoring, apiVersion: V1, resource: Facilities, resourceId: facilityId.ToString(), endpoint: endpoint, queryParams: queryParams);

    private static string GetResourceUrl(string module, string apiVersion, string resource)
        => $"{module}/{apiVersion}/{resource}";

    private static string GetFullUrl(string module, string apiVersion, string resource, string resourceId, string endpoint, NameValueCollection queryParams)
        => $"{GetResourceUrl(module, apiVersion, resource)}/{resourceId}/{endpoint}{queryParams.ToQueryString()}";
}
