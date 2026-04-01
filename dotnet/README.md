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

## License

This SDK is licensed under the [MIT License](LICENSE).
