using HeimdallPower.Api.Client;
using HeimdallPower.Api.Client.Assets;

// Configuration setup
const string clientId = "insert-your-client-id-here";
const string clientSecret = "insert-your-client-secret-here";

Console.WriteLine("Initiating Heimdall API client");

// Instantiate Cloud API Client
var api = new HeimdallApiClient(clientId, clientSecret);

// Fetch Lines data
var assets = await api.GetAssetsAsync();
var line = assets.AllLines().FirstOrDefault();
if (line == null)
{
    Console.WriteLine("No lines found");
    return;
}

Console.WriteLine($"Using line: {line.Name} (ID: {line.Id})");

// Fetch Aggregated Measurements data
var latestCurrent = await api.GetLatestCurrentAsync(line.Id);
var latestConductorTemperature = await api.GetLatestConductorTemperatureAsync(line.Id);
var latestIcing = await api.GetLatestIcingAsync(line.Id);

Console.WriteLine($"- Current: {latestCurrent.Current.Value} {latestCurrent.Unit} at {latestCurrent.Current.Timestamp}");
Console.WriteLine($"- Conductor Temperature: {latestConductorTemperature.ConductorTemperature.Max} {latestConductorTemperature.Unit} at {latestConductorTemperature.ConductorTemperature.Timestamp}");
Console.WriteLine($"- Icing: Maximum Ice weight: {latestIcing.Icing.Max.IceWeight} at span phase: {latestIcing.Icing.Max.IceWeight.SpanPhaseId}");

// Fetch DLR data
var latestDlr = await api.GetLatestHeimdallDlrAsync(line.Id);
var latestAar = await api.GetLatestHeimdallAarAsync(line.Id);
var forecastDlr = await api.GetHeimdallDlrForecastsAsync(line.Id);
var forecastAar = await api.GetHeimdallAarForecastsAsync(line.Id);

Console.WriteLine($"- Heimdall DLR: {latestDlr.HeimdallDlr.Value} {latestDlr.Unit} at {latestDlr.HeimdallDlr.Timestamp}");
Console.WriteLine($"- Heimdall AAR: {latestAar.HeimdallAar.Value} {latestAar.Unit} at {latestAar.HeimdallAar.Timestamp}");

// Fetch Circuit Rating data
var facilities = assets.AllFacilities();
var facility = facilities.First(f => f.Line != null && f.Line.Name.Equals(line.Name));

var circuitRating = await api.GetLatestCircuitRatingAsync(facility.Id);
var circuitRatingForecast = await api.GetCircuitRatingForecastsAsync(facility.Id);

Console.WriteLine($"- Circuit Rating: {circuitRating.CircuitRating.Value} {circuitRating.Unit} at {circuitRating.CircuitRating.Timestamp}");
