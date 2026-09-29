# Heimdall API SDK for .NET

Official .NET SDK for the Heimdall Power External API.

## Documentation

- [Getting started](https://developer.heimdallcloud.com/docs/welcome) and [authentication](https://developer.heimdallcloud.com/docs/authentication)
- [Concepts](https://developer.heimdallcloud.com/docs/concepts): assets, measurement points and API modules.
- [Use cases](https://developer.heimdallcloud.com/docs/use-cases): integration flows, [aggregation](https://developer.heimdallcloud.com/docs/use-cases#aggregation) and polling cadence.
- [User Guide](https://heimdallbrain.atlassian.net/servicedesk/customer/portal/1/article/4095541249) (customer login required): DLR and fallback rating details.
- [Examples](examples)

## Installation

```bash
dotnet add package HeimdallPower.Api.Client
```

For DI registration and built-in retry, also add the Extensions package:

```bash
dotnet add package HeimdallPower.Api.Client.Extensions
```

## Quick start

```csharp
using HeimdallPower.Api.Client;

var client = new HeimdallApiClient("your-client-id", "your-client-secret");
var assets = await client.GetAssetsAsync();
```

With the Extensions package:

```csharp
using HeimdallPower.Api.Client;
using HeimdallPower.Api.Client.Extensions;
using Microsoft.Extensions.DependencyInjection;

var services = new ServiceCollection();
services.AddHeimdallPowerApiClient(options =>
{
    options.ClientId = "your-client-id";
    options.ClientSecret = "your-client-secret";
});

var client = services.BuildServiceProvider().GetRequiredService<IHeimdallApiClient>();
```

## Iterate over instrumented lines

Not every line has Neurons installed.
Data endpoints return 404 or no data for lines without active measurement points.
`GetInstrumentedLinesAsync` returns only lines with at least one active measurement point, with their facility.

```csharp
using HeimdallPower.Api.Client.Assets;

foreach (var instrumented in await client.GetInstrumentedLinesAsync())
{
    var current = await client.GetLatestCurrentAsync(instrumented.Line.Id);
    Console.WriteLine($"{instrumented.Facility.Name} / {instrumented.Line.Name}: {current.Current.Value} {current.Unit}");
}
```

Already have the assets? Use `assets.InstrumentedLines()`.

## Optional parameters

- Required inputs (ids, time ranges) are positional.
- Optional inputs go in a per-method options record, e.g. `GetLatestCurrentAsync` takes `GetLatestCurrentOptions`.
- Pass `null` or leave it out for the defaults.
- New optional API parameters become new properties, so existing code keeps compiling.

```csharp
using HeimdallPower.Api.Client;
using HeimdallPower.Api.Client.CapacityMonitoring;
using HeimdallPower.Api.Client.GridInsights.Lines;

var dlr = await client.GetLatestHeimdallDlrAsync(lineId, new() { Quantity = Quantity.ApparentPower, Since = DateTimeOffset.UtcNow.AddMinutes(-15) });
var temperatures = await client.GetConductorTemperaturesAsync(lineId, from, to, new() { UnitSystem = UnitSystem.Imperial, Include = ConductorTemperatureInclude.MeasurementPoints });
```

## Proxy configuration

Configure an outbound HTTP proxy via `ProxyOptions`:

```csharp
services.AddHeimdallPowerApiClient(options =>
{
    options.ClientId = "your-client-id";
    options.ClientSecret = "your-client-secret";
    options.Proxy = new ProxyOptions
    {
        Address = "http://proxy.example.com:8080",
        Username = "proxy-user",     // optional
        Password = "proxy-password", // optional
    };
});
```

- Without an explicit `Address`, the SDK uses the `HTTPS_PROXY`/`HTTP_PROXY`/`NO_PROXY` environment variables.
- The proxy applies to both API calls and token acquisition.

## Error handling

### Resilience and retry

- **The core package does not retry.** A directly created `HeimdallApiClient` throws transient errors (502/503/504) immediately as `HeimdallApiException`.
- **The Extensions package adds resilience** via [`AddStandardResilienceHandler`](https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience). `AddHeimdallPowerApiClient` enables this pipeline:

| Layer | Behaviour |
|---|---|
| Retry | Up to **3 retries** with exponential back-off + jitter on all 5xx codes, 408, 429, and `HttpRequestException` |
| Circuit breaker | Opens after sustained failures to avoid hammering an unavailable service |
| Total request timeout | Caps the total time including retries |

### Exceptions

| Exception | When |
|---|---|
| `HeimdallApiException` | Non-success HTTP status. `StatusCode` holds the status, `RequestUrl` the request, and `Title`, `Detail` and `Errors` the problem details. |
| `UnauthorizedAccessException` | Authentication failed after a token-refresh attempt. |
| `OperationCanceledException` | The provided `CancellationToken` was cancelled. |

```csharp
using System.Net;

try
{
    var dlr = await client.GetLatestHeimdallDlrAsync(lineId);
}
catch (HeimdallApiException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
{
    // No data for the line in the requested window, or unknown line
}
catch (HeimdallApiException ex) when (ex.StatusCode == HttpStatusCode.BadRequest)
{
    // Validation error, e.g. ex.Errors["since"]
}
catch (HeimdallApiException ex)
{
    // Other API error — ex.StatusCode contains the HTTP status
}
```

### Cancellation and timeouts

Every method accepts an optional `CancellationToken`.

```csharp
// Cancel after 10 seconds total
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
var dlr = await client.GetLatestHeimdallDlrAsync(lineId, cancellationToken: cts.Token);
```

For a per-request timeout, pass an `HttpClient` with `Timeout` set via `HeimdallApiClientSettings`:

```csharp
var httpClient = new HttpClient
{
    BaseAddress = new Uri("https://external-api.heimdallcloud.com"),
    Timeout = TimeSpan.FromSeconds(5),
};
var client = new HeimdallApiClient(clientId, clientSecret, new HeimdallApiClientSettings { HttpClient = httpClient });
```

## License

This SDK is licensed under the [Apache License 2.0](../LICENSE).
