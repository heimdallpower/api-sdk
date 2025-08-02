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

More examples can be seen in the [examples folder](examples).
