using HeimdallPower.Api.Client;

// Configuration setup
var clientId = "insert-your-client-id-here";
var clientSecret = "insert-your-client-secret-here";
var lineName = "insert-line-name-here";

Console.WriteLine("Initiating Heimdall API example client");

// Instantiate Cloud API Client
var api = new HeimdallApiClient(clientId, clientSecret);

// Fetch Lines data
var lines = await api.GetLines();
var line = lines.FirstOrDefault(line => (bool)line?.Name.Equals(lineName));

// Fetch Facilities data
var facilities = await api.GetFacilities();
var facility = facilities.FirstOrDefault(f => (bool)f.Line?.Name.Equals(lineName));

if (line != null)
{
    // Fetch Aggregated Measurements data
    var latestCurrent = await api.GetLatestCurrent(line.Id);
    var latestConductorTemperature = await api.GetLatestConductorTemperature(line.Id);

    // Fetch DLR data
    var latestHeimdallDlr = await api.GetLatestHeimdallDlr(line.Id);
    var latestHeimdallAar = await api.GetLatestHeimdallAar(line.Id);
    var heimdallDlrForecasts = await api.GetHeimdallDlrForecasts(line.Id);
    var heimdallAarForecasts = await api.GetHeimdallAarForecasts(line.Id);
}

if (facility != null)
{
    // Fetch Circuit Rating data
    var circuitRatingForecast = await api.GetCircuitRatingForecasts(facility.Id);
    var latestCircuitRating = await api.GetLatestCircuitRating(facility.Id);
}
