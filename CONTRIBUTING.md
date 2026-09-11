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
- The two SDKs are **versioned and released independently**, each from its own tag:
  - .NET (`HeimdallPower.Api.Client`, `HeimdallPower.Api.Client.Extensions` → NuGet): `dotnet-v<MAJOR>.<MINOR>.<PATCH>[-<prerelease>]`, e.g. `dotnet-v4.1.0`, `dotnet-v4.2.0-beta.1`
  - Python (`heimdallpower-api-client` → PyPI): `python-v<MAJOR>.<MINOR>.<PATCH>[-(alpha|beta|rc).<N>]`, e.g. `python-v4.1.0`, `python-v4.2.0-rc.1` (the suffix must be valid PEP 440; `-test` is not)
- The version lives **only in the tag**. `<Version>0.0.0</Version>` and `version = "0.0.0"` in the repo are placeholders that CI overrides; do not bump them.
- A change that touches both SDKs gets **two releases**, one per tag.
- The unprefixed `vX.Y.Z` format (up to `v4.0.0`) is retired. Publishing a Release on a **newly created** `vX.Y.Z` tag now fails both publish workflows on purpose. Note that pushing such a tag by itself does nothing — the publish workflows trigger on Release *publication*, not on a tag push. And never re-publish a Release on one of the **pre-existing** `v*` tags (`v1.0.0`…`v4.0.0`): those commits predate the tag guard and still run the old, unsplit, unguarded publish workflows from that commit.

### Cutting a release

1. Run the **Prepare release (draft)** workflow (Actions → *Prepare release (draft)* → *Run workflow*), choose the SDK, optionally type a version. It computes the baseline from the highest existing `<sdk>-v*` tag (falling back to the legacy `v*` tag before any prefixed tag exists) and diffs `HEAD` against it. On success it creates a draft release with the proposed tag, `--target` pinned to the commit you dispatched from, and generated notes. If it finds no `feat`/`fix`/breaking commits for that SDK since the baseline, it prints its report and exits **without drafting anything** — pass a version override to force a release anyway.
   - The suggested bump is **advisory only**: it comes from conventional-commit **subject lines** (plus a `BREAKING CHANGE:`/`BREAKING-CHANGE:` footer) since the baseline tag — dependency-bump commit *bodies* that embed another project's changelog are ignored. A `chore:` that breaks consumers (as the .NET 10 upgrade did) is invisible to it. Decide the number yourself.
   - It also reports commits that touch files outside both SDKs' path sets (check whether they matter) and unreleased commits on the *other* SDK (so a paired change is not forgotten).
   - If the proposed tag **already exists**, it refuses to draft (`::error::`) — a published version can't be re-targeted this way.
   - If you pass a version override and there are no matching changes, it still drafts, but emits a `::warning::` and says so in the release notes body — check that this is really what you meant before publishing.
   - Iterating a prerelease (e.g. `rc.1` → `rc.2`) needs a manual version override: the baseline always tracks the last *stable* tag by design, so the helper won't notice an existing prerelease on its own.
2. Open the draft, review the notes and the version. **Do not click "Generate release notes"** — GitHub compares against the chronologically previous release, which under a split is often the *other* SDK's.
3. Publish. Publishing creates the tag, which triggers `nuget-publish.yml` or `python-publish.yml`; the other one skips. Both use trusted publishing (OIDC) — no stored API tokens.
4. Nothing published to NuGet or PyPI can be re-used: a wrong version number is permanent. Check twice.

> **Never delete a release tag.** The tag is the only record that a version number has been burned — both the reuse refusal in step 1 and the version baseline it computes from read tags, so deleting one silently un-burns that version and the helper will happily re-propose it. For NuGet this is especially quiet: `nuget-publish.yml` pushes with `--skip-duplicate`, so re-publishing an already-shipped version exits 0 having uploaded nothing — a green workflow and release notes claiming a version shipped, with nothing actually new on nuget.org.

> The **Latest** badge / `releases/latest` on the Releases page now alternates between whichever SDK shipped most recently. Link to explicit tags, never to `releases/latest`.

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
