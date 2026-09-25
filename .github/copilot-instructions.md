# api-sdk AI Coding Agent Instructions

## Project Overview

Official .NET and Python SDKs for the Heimdall Power External API. Each SDK is versioned and released independently from its own tag. The API contract is defined by the public OpenAPI specs at `https://external-api.heimdallcloud.com/openapi/{module}/v1/openapi.yaml` (`assets`, `capacity_monitoring`, `grid_insights`).

## Domain Understanding

Heimdall Power monitors overhead power lines with sensors ("Neurons") mounted on the conductors.

| Term                  | Meaning                                                                |
| --------------------- | ---------------------------------------------------------------------- |
| Grid owner            | Utility that owns the lines; the API scopes all data to it             |
| Line / span / span phase | Line between substations → section between towers → one conductor phase |
| Measurement point     | Neuron location on a span phase; `include=measurement_points` breaks data down to it |
| Facility              | Substation or similar; circuit ratings are per facility                |
| Heimdall DLR / AAR    | Dynamic line rating / ambient-adjusted rating (capacity)               |
| Transient rating      | Short-term emergency rating                                            |
| `quantity`            | `current` (A) or `apparent_power` (MVA) for ratings                    |
| `since`               | Cut-off for "latest" endpoints — older data is excluded                |

API modules: `assets`, `capacity_monitoring`, `grid_insights`. Every request carries the `x-region` header.

## Key Conventions

- .NET and Python stay in parity — see the [`sdk-review`](skills/sdk-review/SKILL.md) parity checks.
- Python `*_api_client/` packages are generated — never edited by hand — see [python conventions](instructions/python.instructions.md).
- .NET DTOs and URLs are hand-written — see [.NET conventions](instructions/dotnet.instructions.md).
- Versions come only from `dotnet-v*` / `python-v*` tags — see [release conventions](instructions/release.instructions.md).

## Code Review Behavior

When reviewing pull requests:

- Only comment when you have HIGH CONFIDENCE (>80%) that an issue exists.
- Be concise: one sentence per comment when possible. Include: problem, why it matters, fix.
- Do NOT comment on: formatting, style preferences, naming bikeshedding, or things covered by CI.

### Priority Areas (flag these)

- Breaking public API not marked per the [release conventions](instructions/release.instructions.md#versioning) — the release helper then under-bumps the version
- Optional parameters inserted before `cancellationToken` without a migration note
- Endpoint, parameter, or field added to one SDK but not the other, with no stated reason
- SDK behavior that contradicts the OpenAPI spec (names, types, required/nullable, enum values, timestamp format)
- Hand edits inside `python/heimdall_api_client/*_api_client/`
- Timestamps not sent as ISO 8601 UTC (`Z`)
- New endpoints or parameters without unit tests asserting the query string and parsed response
- Hardcoded credentials or tokens

### What CI Already Covers (skip these)

- Build and compile errors, unit test failures
- Ruff lint and formatting, `poetry.lock` sync
- PR title format (Conventional Commits)

## Behavioral Guidance

See `AGENTS.md` at the repository root for behavioral expectations and governance constraints. This file provides domain context only.
