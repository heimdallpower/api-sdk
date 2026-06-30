# Heimdall API SDK for .NET

This folder contains the official .NET SDK for accessing the [Heimdall Power External API](https://developer.heimdallcloud.com/docs/welcome).

The SDK simplifies authentication and interaction with the External API using strongly-typed C# clients.

---

## Installation

The package is available on [NuGet](https://www.nuget.org/profiles/heimdall_power):

```bash
dotnet add package HeimdallPower.Api.Client
```

If you want DI integration and built-in resiliency (including retry), also install the Extensions package:

```bash
dotnet add package HeimdallPower.Api.Client.Extensions
```

### Usage Example

```csharp
using HeimdallPower.Api.Client;

var clientId = "your-client-id";
var clientSecret = "your-client-secret";

var heimdallApiClient = new HeimdallApiClient(clientId, clientSecret);

```

Using the optional HeimdallPower.Api.Client.Extensions package:

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

var provider = services.BuildServiceProvider();
var heimdallApiClient = provider.GetRequiredService<HeimdallApiClient>();
```

You can also inject `IHeimdallApiClient` for the abstraction.

More examples can be seen in the [examples folder](examples).

### Proxy Configuration

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

When no explicit `Address` is set, the SDK falls back to `HTTPS_PROXY`/`HTTP_PROXY`/`NO_PROXY` environment variables. The proxy applies to both API calls and token acquisition.

## Error Handling

### Resilience and retry

**`HeimdallPower.Api.Client` (core package) does not retry automatically.** If you instantiate `HeimdallApiClient` directly (without DI), transient gateway errors such as 502/503/504 are thrown immediately as `HeimdallApiException`. Your application is responsible for any retry logic.

**`HeimdallPower.Api.Client.Extensions` (DI package) adds full resilience** via [`AddStandardResilienceHandler`](https://learn.microsoft.com/en-us/dotnet/core/resilience/http-resilience) from `Microsoft.Extensions.Http.Resilience`. When you register the client with `AddHeimdallPowerApiClient`, the following pipeline is active automatically:

| Layer | Behaviour |
|---|---|
| Retry | Up to **3 retries** with exponential back-off + jitter on all 5xx codes, 408, 429, and `HttpRequestException` |
| Circuit breaker | Opens after sustained failures to avoid hammering an unavailable service |
| Total request timeout | Caps the total time including retries |

```csharp
// Retries are handled automatically — no extra code needed.
var dlr = await client.GetLatestHeimdallDlrAsync(lineId);
```

### Exceptions

| Exception | When |
|---|---|
| `HeimdallApiException` | Non-success HTTP error (400, 403, 404, 500, 502, …). Check `StatusCode` for the HTTP status. |
| `UnauthorizedAccessException` | Authentication failed after a token-refresh attempt. |
| `OperationCanceledException` | The provided `CancellationToken` was cancelled. |

```csharp
try
{
    var dlr = await client.GetLatestHeimdallDlrAsync(lineId);
}
catch (HeimdallApiException ex) when (ex.StatusCode == HttpStatusCode.NotFound)
{
    // Line not found
}
catch (HeimdallApiException ex)
{
    // Other API error — ex.StatusCode contains the HTTP status
}
```

### Cancellation and timeouts

Every method accepts an optional `CancellationToken`. Cancellation is respected during the HTTP request.

```csharp
// Cancel after 10 seconds total
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
var dlr = await client.GetLatestHeimdallDlrAsync(lineId, cancellationToken: cts.Token);
```

To set a per-request HTTP timeout, configure `HttpClient.Timeout` and pass it to the constructor:

```csharp
var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(5) };
var client = new HeimdallApiClient(clientId, clientSecret, httpClient: httpClient);
```

## License

This SDK is licensed under the [MIT License](LICENSE).
