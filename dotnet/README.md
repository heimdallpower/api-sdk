# Heimdall API SDK for .NET

This folder contains the official .NET SDK for accessing the [Heimdall Power External API](https://developer.heimdallcloud.com/docs/welcome).

The SDK simplifies authentication and interaction with the External API using strongly-typed C# clients.

---

## Installation

The package is available on NuGet:

```bash
dotnet add package HeimdallPower.Api.Client --version <latest_version>
```

Replace <latest_version> with the latest version from [NuGet](https://www.nuget.org/packages/HeimdallPower.Api.Client).

### Usage Example

```csharp
﻿using HeimdallPower.Api.Client;

var clientId = "insert-your-client-id-here";
var clientSecret = "insert-your-client-secret-here";

var heimdallApiclient = new HeimdallApiClient(clientId, clientSecret);

```

More examples can be seen in the [examples folder](examples).
