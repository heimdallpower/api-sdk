---
applyTo: "dotnet/**"
---

# .NET SDK — Conventions

Conventions only. For the workflow of adding API changes, see *Updating the SDK for API changes* in `CONTRIBUTING.md`.

## Layout

| Path (under `dotnet/`)                                            | Contents                                                |
| ----------------------------------------------------------------- | ------------------------------------------------------- |
| `HeimdallPower.Api.Client/HeimdallPower.Api.Client/`               | Core SDK, `net10.0`, nullable enabled                   |
| `…/IHeimdallApiClient.cs`, `…/HeimdallApiClient.cs`                | Public surface — one async method per operation         |
| `…/UrlBuilder.cs`, `…/UrlBuilder.Extensions.cs`                    | Route constants, `Build…Url`, query param helpers       |
| `…/{Assets,CapacityMonitoring,GridInsights}/`                      | Responses and DTOs, grouped by API module and resource |
| `HeimdallPower.Api.Client/HeimdallPower.Api.Client.Extensions/`    | DI registration, resilience, proxy options              |
| `tests/unit/…UnitTests/`, `tests/integration/…IntegrationTests/`   | `When…` folders, one class per scenario                 |
| `examples/Api.Client.Examples/`                                    | Runnable usage examples                                 |

## Rules

| Rule                                                                 | Why                                              |
| -------------------------------------------------------------------- | ------------------------------------------------ |
| No code generation — DTOs mirror the spec by hand                    | Drift is only caught by review and tests         |
| PascalCase DTO properties; `HeimdallApiHttpClient` uses `SnakeCaseLower` | Maps to the `snake_case` wire contract        |
| Method shape: `(id, …required, …optional, CancellationToken cancellationToken = default)` | Existing style across the interface |
| New optional params go before `cancellationToken` → breaking (`!`)   | Positional tokens and implementers break         |
| Add to `IHeimdallApiClient` and `HeimdallApiClient` together         | Interface is the mockable contract               |
| Query params added only when set (no `include=`, no bare `?`)        | Unset means "server default", not empty         |
| Timestamps via `UrlBuilder.ToApiTimestamp` (UTC, `Z`)                | Never `ToString()` — culture-dependent           |
| Enum query values as dedicated enums (e.g. `CurrentInclude`)         | Typed, discoverable options                      |
| XML docs on every public member, copied in meaning from the spec     | IntelliSense is the SDK's documentation          |

## Tests

| Kind        | Trait                          | Pattern                                                                 |
| ----------- | ------------------------------ | ----------------------------------------------------------------------- |
| Unit        | `[Trait("Category", "Unit")]`  | Public method via the recording fake transport in `Fakes/`; assert query string and deserialized fields |
| Integration | `[Trait("Category", "Integration")]` | Real API, needs `HEIMDALL_CLIENT_ID`/`HEIMDALL_CLIENT_SECRET`; runs on `main` |

Commands: `dotnet test --filter Category=Unit` (CI) and `--filter Category=Integration` (credentials).

Writing tests: `sdk-write-unit-tests` and `sdk-write-integration-tests` skills.
