# Contributing to Heimdall Power API SDK

This repo contains two independently released SDKs for the [Heimdall Power External API](https://developer.heimdallcloud.com/docs/welcome):

| Folder | Package | Published to |
|---|---|---|
| `dotnet/` | `HeimdallPower.Api.Client` (+ `.Extensions`) | NuGet |
| `python/` | `heimdallpower-api-client` | PyPI |

Most changes touch only one of them.

## Commits & pull requests

Commit messages and PR titles follow [Conventional Commits](https://www.conventionalcommits.org/). **PR titles are validated by CI** — a non-conforming title fails the check.

```
type(scope): description
```

- **Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`, `build`, `style`, `perf`
- **Scope** (optional): use when the change is module-specific — `python`, `dotnet`
- **Description:** imperative, lowercase, no trailing period. Include the Jira ticket if there is one.
- Mark breaking changes with `!` (`feat(dotnet)!: ...`) or a `BREAKING CHANGE:` footer.

```
feat(dotnet): POWER-4075 add proxy configuration for API client
fix(python): handle missing auth token gracefully
docs: update contributing guidelines
```

PRs target `main` and need a review from a code owner — `@heimdallpower/backend` is requested automatically.

## Branching & Releases

The two SDKs are **versioned and released independently**, each from its own tag:

| SDK | Tag format | Examples |
|---|---|---|
| .NET | `dotnet-v<MAJOR>.<MINOR>.<PATCH>[-prerelease]` | `dotnet-v4.1.0`, `dotnet-v4.2.0-beta.1` |
| Python | `python-v<MAJOR>.<MINOR>.<PATCH>[-(alpha\|beta\|rc).<N>]` | `python-v4.1.0`, `python-v4.2.0-rc.1` |

- The version lives **only in the tag**. The `0.0.0` values in the `.csproj` files and `pyproject.toml` are placeholders that CI overrides — don't bump them.
- A change touching both SDKs gets **two releases**, one per tag.
- Python prereleases accept only `-alpha.N`, `-beta.N` and `-rc.N`. Other PEP 440 spellings (`-preview`, `-pre`, `-a1`) are rejected by the guard, and `-test` isn't PEP 440 at all.
- The unprefixed `vX.Y.Z` format is retired — a release on a new one fails both publish workflows on purpose. Don't re-publish on the old `v1.0.0`–`v4.0.0` tags either: those commits predate the guard and still run the unsplit workflows.

### Cutting a release

1. **Actions → *Prepare release (draft)* → Run workflow.** Pick the SDK and leave the version blank to accept the suggestion. It creates a draft pinned to the commit you dispatched from, or exits without drafting if that SDK has nothing to release. Iterating a prerelease (`rc.1` → `rc.2`) needs an explicit version.
2. **Review the draft.** The suggested bump is **advisory** — it reads commit subjects, so a breaking change typed `chore:` looks safe to it. If the number is wrong, re-run step 1 with an explicit version and delete the superseded draft.
3. **Publish the draft.** You don't create the tag yourself: the draft holds the tag name and the commit it points at, and GitHub creates the tag when you publish. That fires `nuget-publish.yml` or `python-publish.yml`; the other skips. Both use trusted publishing (OIDC) — no stored API tokens.

Before publishing:

- **Don't click *Generate release notes*.** GitHub compares against the chronologically previous release, which under a split is usually the *other* SDK's.
- **Never delete a release tag.** It's the only record that a version number is burned, and the helper reads tags to refuse reuse.
- **A published version can never be reused** on NuGet or PyPI. Check the number twice — NuGet pushes with `--skip-duplicate`, so a repeat exits 0 having uploaded nothing.
- Link to explicit tags, never `releases/latest` — it now alternates between the two SDKs.

## Python

Requires Python 3.11+ and [Poetry](https://python-poetry.org/).

```bash
poetry install --with dev          # set up
poetry run ruff check . --fix      # lint
poetry run ruff format .           # format
poetry run pytest                  # unit tests
poetry run pytest -m integration   # integration tests (needs credentials)
poetry build                       # build .whl and .tar.gz
```

> The `*_api_client` subdirectories under `python/heimdall_api_client/` are **auto-generated** from OpenAPI specs. Don't edit them by hand — regenerate instead. They're excluded from ruff.

To regenerate a module's client:

```bash
cd python/scripts
./generate-module-client.ps1 -Module assets
```

This downloads the OpenAPI spec and writes the client to `python/heimdall_api_client/<module>`.

## .NET

- `HeimdallPower.Api.Client` — core SDK library
- `HeimdallPower.Api.Client.Extensions` — DI integration and resilience extensions
- `tests/` — unit and integration tests

```bash
dotnet test --filter Category=Unit          # unit tests
dotnet test --filter Category=Integration   # integration tests (needs credentials)
```

Integration tests for both SDKs require `HEIMDALL_CLIENT_ID` and `HEIMDALL_CLIENT_SECRET`.
