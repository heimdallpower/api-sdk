# Heimdall API SDK for .NET

This folder contains the official .NET SDK for accessing the [Heimdall Power External API](https://developer.heimdallcloud.com/docs/welcome).

The SDK simplifies authentication and interaction with the External API using strongly-typed C# clients.

---

## Installation

The package is available on [NuGet](https://www.nuget.org/profiles/heimdall_power):

```bash
dotnet add package HeimdallPower.Api.Client
```

If you want DI integration and built-in resiliency, install:

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

## Error Handling and Retry

The SDK handles transient infrastructure errors automatically so your application does not have to.

### Automatic retry

All API methods retry **up to 3 times** with **exponential backoff** (1 s → 2 s → 4 s) on the following transient conditions:

| Condition | Description |
|---|---|
| `502 Bad Gateway` | Reverse proxy / Application Gateway could not reach the upstream server |
| `503 Service Unavailable` | Server temporarily unavailable |
| `504 Gateway Timeout` | Upstream server did not respond in time |
| `HttpRequestException` | Network-level failure (DNS, connection refused, etc.) |

If all 3 retry attempts are exhausted, a `HeimdallApiException` is thrown with the status code of the last failed response.

> **Note:** `500 Internal Server Error` is **not** retried as it typically indicates a permanent application-level error.

### Exceptions

| Exception | When |
|---|---|
| `HeimdallApiException` | Non-transient HTTP error (400, 403, 404, 500, …). Check `StatusCode` for the HTTP status. |
| `UnauthorizedAccessException` | Authentication failed after a token-refresh attempt. |
| `OperationCanceledException` | The provided `CancellationToken` was cancelled (including during a retry delay). |

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

Every method accepts an optional `CancellationToken`. Cancellation is respected both during the HTTP request **and** during retry backoff delays.

```csharp
// Cancel after 10 seconds total (including any retries)
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
var dlr = await client.GetLatestHeimdallDlrAsync(lineId, cancellationToken: cts.Token);
```

To set a per-request HTTP timeout (independent of retries), configure `HttpClient.Timeout` and pass it to the constructor:

```csharp
var httpClient = new HttpClient { Timeout = TimeSpan.FromSeconds(5) };
var client = new HeimdallApiClient(clientId, clientSecret, httpClient: httpClient);
```

## License

This SDK is licensed under the [MIT License](LICENSE).
