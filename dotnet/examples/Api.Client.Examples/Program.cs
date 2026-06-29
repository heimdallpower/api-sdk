using HeimdallPower.Api.Client;
using HeimdallPower.Api.Client.Assets;

// Configuration setup
const string clientId = "insert-your-client-id-here";
const string clientSecret = "insert-your-client-secret-here";

Console.WriteLine("Initiating Heimdall API client");

// Instantiate Cloud API Client
// Note: direct instantiation does NOT include automatic retry.
// Use HeimdallPower.Api.Client.Extensions (AddHeimdallPowerApiClient) for built-in resilience.
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

var from = DateTimeOffset.Now.AddDays(-1);
var to = DateTimeOffset.Now;

// Fetch Aggregated Measurements data
var latestCurrent = await api.GetLatestCurrentAsync(line.Id);
var currents = await api.GetCurrentsAsync(line.Id, from, to);

Console.WriteLine($"- Current: {latestCurrent.Current.Value} {latestCurrent.Unit} at {latestCurrent.Current.Timestamp}");
Console.WriteLine($"- Currents from {from} to {to} - First value: {currents.Currents.FirstOrDefault()?.Value} {currents.Unit} at {currents.Currents.FirstOrDefault()?.Timestamp}, " +
                  $"Last value: {currents.Currents.LastOrDefault()?.Value} {currents.Unit} at {currents.Currents.LastOrDefault()?.Timestamp}");

var latestConductorTemperature = await api.GetLatestConductorTemperatureAsync(line.Id);
var conductorTemperatures = await api.GetConductorTemperaturesAsync(line.Id, from, to);

Console.WriteLine($"- Conductor Temperature: {latestConductorTemperature.ConductorTemperature.Max} {latestConductorTemperature.Unit} at {latestConductorTemperature.ConductorTemperature.Timestamp}");
Console.WriteLine($"- Conductor Temperatures from {from} to {to} - First max value: {conductorTemperatures.ConductorTemperatures.FirstOrDefault()?.Max} {conductorTemperatures.Unit} at {conductorTemperatures.ConductorTemperatures.FirstOrDefault()?.Timestamp}, " +
                  $" Last max value: {conductorTemperatures.ConductorTemperatures.LastOrDefault()?.Max} {conductorTemperatures.Unit} at {conductorTemperatures.ConductorTemperatures.LastOrDefault()?.Timestamp}");

var latestIcing = await api.GetLatestIcingAsync(line.Id);
var icings = await api.GetIcingsAsync(line.Id, from, to);

Console.WriteLine($"- Icing: Maximum Ice weight: {latestIcing.Icing.Max.IceWeight.Value} at span phase: {latestIcing.Icing.Max.IceWeight.SpanPhaseId}");
Console.WriteLine($"- Icing from {from} to {to} - Max Ice weight: {icings.Icing.Max.IceWeight.Value} {icings.Icing.Max.IceWeight.Unit} at span phase: {icings.Icing.Max.IceWeight.SpanPhaseId}");

var latestSagAndClearance = await api.GetLatestSagAndClearanceAsync(line.Id);
var sagAndClearances = await api.GetSagAndClearancesAsync(line.Id, from, to);

Console.WriteLine($"- Sag and Clearance: Maximum sag: {latestSagAndClearance.SagAndClearance.MaxSag.Value} {latestSagAndClearance.SagAndClearance.MaxSag.Unit} at span phase: {latestSagAndClearance.SagAndClearance.MaxSag.SpanPhaseId}");
Console.WriteLine($"- Sag and Clearance from {from} to {to} - Max Sag: {sagAndClearances.SagAndClearance.MaxSag.Value} - Min Clearance: {sagAndClearances.SagAndClearance.MinClearance?.Value}");

// Fetch DLR data
var latestDlr = await api.GetLatestHeimdallDlrAsync(line.Id);
var latestAar = await api.GetLatestHeimdallAarAsync(line.Id);
var forecastDlr = await api.GetHeimdallDlrForecastsAsync(line.Id);
var forecastAar = await api.GetHeimdallAarForecastsAsync(line.Id);

Console.WriteLine($"- Heimdall DLR: {latestDlr.HeimdallDlr.Value} {latestDlr.Unit} at {latestDlr.HeimdallDlr.Timestamp} with IsFallback={latestDlr.HeimdallDlr.IsFallback}");
Console.WriteLine($"- Heimdall AAR: {latestAar.HeimdallAar.Value} {latestAar.Unit} at {latestAar.HeimdallAar.Timestamp}");

// Fetch Circuit Rating data
var facilities = assets.AllFacilities();
var facility = facilities.First(f => f.Line != null && f.Line.Name.Equals(line.Name));

var circuitRating = await api.GetLatestCircuitRatingAsync(facility.Id);
var circuitRatingForecast = await api.GetCircuitRatingForecastsAsync(facility.Id);

var limitingComponent = circuitRating.CircuitRating.AtFacilityComponentId.HasValue
    ? facility.Components.FirstOrDefault(c => c.Id == circuitRating.CircuitRating.AtFacilityComponentId.Value)?.Name ?? "unknown"
    : "none";
Console.WriteLine($"- Circuit Rating: {circuitRating.CircuitRating.Value} {circuitRating.Unit} at {circuitRating.CircuitRating.Timestamp}, limiting component: {limitingComponent}, IsFallback={circuitRating.CircuitRating.IsFallback}");

// Example: wrapping a single call with error handling.
try
{
    var dlr = await api.GetLatestHeimdallDlrAsync(line.Id);
    Console.WriteLine($"DLR: {dlr.HeimdallDlr.Value} {dlr.Unit}");
}
catch (HeimdallApiException ex)
{
    Console.Error.WriteLine($"API error {(int)ex.StatusCode}: {ex.Message}");
}

// Example: cancel the request after 10 seconds total.
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
var dlrWithTimeout = await api.GetLatestHeimdallDlrAsync(line.Id, cancellationToken: cts.Token);
Console.WriteLine($"DLR with timeout: {dlrWithTimeout.HeimdallDlr.Value} {dlrWithTimeout.Unit}");

