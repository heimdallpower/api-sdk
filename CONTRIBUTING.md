# Contributing to Heimdall Power API SDK

Thank you for your interest in contributing!

This repository contains SDKs and example clients for accessing the [Heimdall Power External API](https://developer.heimdallcloud.com/docs/welcome).

---

## Conventional Commits

This project follows the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages and PR titles.

**PR titles are validated by CI** — a PR with a non-conforming title will fail the status check.

### Format

```
type(scope): description
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build`, `style`, `perf`

**Scope** (optional): use when the change is clearly module-specific, e.g. `python`, `dotnet`.

**Description:** imperative, lowercase, no trailing period. Include the Jira ticket if applicable.

### Examples

```
feat: add new endpoint for circuit ratings
feat(dotnet): POWER-4075 add proxy configuration for API client
fix(python): handle missing auth token gracefully
docs: update contributing guidelines
ci: add conventional commits PR title validation
```

---

## Pull Requests

- PR titles **must** follow the [Conventional Commits](#conventional-commits) format.
- Include a short description of what the PR does and why.
- Pull requests targeting `main` must be reviewed by a **code owner**.

> Heimdall Power's backend team (`@heimdallpower/backend`) is configured as the code owner. Reviews will be automatically requested when a PR is opened.

---

## Branching & Releases

- Contributions should be made as pull requests into `main`.
- Releases are managed using GitHub Releases.
- Tags must follow the format: `v<MAJOR>.<MINOR>.<PATCH>` (e.g., `v1.2.3`)
- A GitHub Release must be published for the package to be built and pushed to NuGet
- The `v` prefix is automatically stripped when packaging

---

## Python

The `python/` folder contains the Python SDK and related utilities.

> **Note:** The `*_api_client` subdirectories under `python/heimdall_api_client/`
> (e.g., `assets_api_client`, `capacity_monitoring_api_client`, `grid_insights_api_client`)
> are **auto-generated** from OpenAPI specs. Do not edit these directly — regenerate
> them using the generation script instead. These directories are excluded from ruff
> linting and formatting.

### Requirements

- Python 3.11+
- Poetry (dependency and build management)

Install dependencies:

```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry --version
poetry install --with dev
```

#### Update dependencies

```bash
poetry update --dry-run  # View available dependency updates
poetry update            # Update all dependencies (does not alter pyproject.toml)
```

### Code Style & Linting

We use [Ruff](https://docs.astral.sh/ruff/) for both linting and formatting.

```bash
poetry run ruff check . --fix     # Lint and auto-fix
poetry run ruff format .          # Format code
poetry run ruff format --check .  # Check formatting (used in CI)
```

### Testing

```bash
poetry run pytest                     # Run all non-integration tests
poetry run pytest -m integration      # Run integration tests (requires credentials)
```

Integration tests require `HEIMDALL_CLIENT_ID` and `HEIMDALL_CLIENT_SECRET` environment variables.

### Building the Package

The SDK is packaged using Poetry. A build step is included in the CI pipeline to validate packaging.

To build locally:

```bash
poetry build
```

This will produce .whl and .tar.gz files.
> Running poetry build locally is recommended to catch issues early, such as missing `__init__.py` files, bad version strings, or invalid metadata.

### Generating Clients from OpenAPI

New modules are generated using openapi-python-client.

To generate a module:

```bash
# Navigate to the script folder and run
./generate_module.ps1 -Module assets
```

This will:

- Download the OpenAPI spec
- Generate a python client for the module
- Place the result under `python/heimdall_api_client/<module>`

---

## .NET

The `dotnet/` folder contains the .NET SDK.

### Project Structure

- `HeimdallPower.Api.Client` — Core SDK library
- `HeimdallPower.Api.Client.Extensions` — DI integration and resilience extensions
- `tests/` — Unit and integration tests

### Running Tests

```bash
dotnet test --filter Category=Unit          # Unit tests only
dotnet test --filter Category=Integration   # Integration tests (requires credentials)
```

Integration tests require `HEIMDALL_CLIENT_ID` and `HEIMDALL_CLIENT_SECRET` environment variables.
