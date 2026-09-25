# AGENTS.md — AI Collaboration Guide for api-sdk

## 1. Purpose and Scope

This file defines behavioral expectations for AI coding agents working in this repository. It applies regardless of tool, IDE, or platform.

**Governance model:** AI assists. Humans decide. Engineers own every merge.

The repo holds two independently released SDKs for the Heimdall Power External API:

| Folder    | Package                                      | Registry | Style                                   |
| --------- | -------------------------------------------- | -------- | --------------------------------------- |
| `dotnet/` | `HeimdallPower.Api.Client` (+ `.Extensions`) | NuGet    | Hand-written client and DTOs            |
| `python/` | `heimdallpower-api-client`                   | PyPI     | Generated `*_api_client/` + thin wrappers |

**Source of truth:** the public External API OpenAPI specs at `https://external-api.heimdallcloud.com/openapi/{module}/v1/openapi.yaml` (`assets`, `capacity_monitoring`, `grid_insights`). The SDKs follow the spec; they never lead it.

---

## 2. How AI Should Operate in This Repository

- **Follow existing patterns.** Find the nearest similar endpoint, DTO, or test and match it.
- **Stay within the task.** No unsolicited refactors, renames, or scope expansion.
- **Keep .NET and Python in parity.** An API change lands in both SDKs, or the gap is stated in the PR.
- **Prefer small, reviewable changes.** One PR per SDK per concern; state the merge order when PRs depend on each other.
- **Surface ambiguity.** If the spec and the API's observed behavior disagree, ask; don't guess.

---

## 3. Working Within Existing Conventions

- **Never hand-edit generated code.** `python/heimdall_api_client/*_api_client/` is regenerated with `python/scripts/generate-module-client.ps1`.
- **Public API is a contract.** Renaming, reordering parameters, or adding interface members is breaking — see [breaking-change rules](.github/skills/sdk-review/references/breaking-changes.md).
- **Versions live only in release tags.** Don't bump the `0.0.0` placeholders in `.csproj` or `pyproject.toml`.
- **Cap search results.** Pass `-m 20` to `grep`/`rg`; raise the limit explicitly when needed.

Language- and pipeline-specific rules live in the instruction files (Section 6).

---

## 4. Execution and Review Expectations

- **All changes go through pull requests.** AI-generated code meets the same review bar as human code.
- **Build and test before proposing changes** — run what CI runs:

    | SDK    | Commands (from the SDK folder)                                                                           |
    | ------ | -------------------------------------------------------------------------------------------------------- |
    | .NET   | `dotnet restore && dotnet build --no-restore && dotnet test --no-build --filter Category=Unit`           |
    | Python | `poetry check && poetry lock && poetry install --with dev && poetry run ruff check . && poetry run ruff format --check . && poetry run pytest tests/unit -v && poetry build` |

- **Write tests for all new code.** Every new endpoint, parameter, or response field gets a unit test in each SDK it touches. Integration tests require API client credentials in `HEIMDALL_CLIENT_ID`/`HEIMDALL_CLIENT_SECRET` and run in CI on pull requests and on push to `main`.
- **Keep commits focused.** Conventional Commits with an SDK scope: `feat(dotnet): …`, `fix(python): …`.
- **Open PRs with the standard template** (`.github/PULL_REQUEST_TEMPLATE.md`); the PR title is validated by CI. PRs are squash-merged; mark breaking changes and fill *Release notes* per the [release conventions](.github/instructions/release.instructions.md#versioning).
- **Respect teammates' PRs.** Add commits on top; never force-push or rewrite someone else's branch.
- **Don't merge, tag, or release.** AI agents propose changes. Humans review, merge, and publish releases.

### Post-Implementation Reviews

After completing any implementation, automatically run the relevant review agents — do not wait to be asked:

| Agent          | Trigger                                              |
| -------------- | ---------------------------------------------------- |
| `sdk-reviewer` | Any change under `dotnet/` or `python/`              |

---

## 5. Handling Uncertainty or Pattern Gaps

Ask for guidance when:

- You're unsure whether to create a **new pattern** or extend an existing one.
- The published spec and the API's behavior **disagree**.
- A change is **breaking** and there is no agreed migration path.
- The change touches **release workflows, tag guards, or publishing** (`.github/workflows/*publish.yml`, `.github/scripts/`).

---

## 6. Instruction Files and Context Sources

| File                                           | Covers                                            |
| ---------------------------------------------- | ------------------------------------------------- |
| `.github/copilot-instructions.md`              | Domain concepts, code review priorities           |
| `.github/instructions/dotnet.instructions.md`  | .NET client layout, DTOs, tests                   |
| `.github/instructions/python.instructions.md`  | Python codegen, wrappers, tests                   |
| `.github/instructions/release.instructions.md` | CI workflows, PR-title check, tags, publishing    |
| `CONTRIBUTING.md`                              | Human-facing contribution and release guide       |

### Skills

Skills are reusable prompt-driven automations in `.github/skills/`. When a task matches a skill below, read the full `.github/skills/<skill>/SKILL.md` and follow its instructions.

**Development skills** — use when performing these tasks:

| Skill                         | Use when…                                                                                                     |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `sdk-write-unit-tests`        | Writing or strengthening .NET/Python unit tests: request/query assertions, parsing, parity, self-review        |
| `sdk-write-integration-tests` | Writing, running or debugging live-API integration tests: credentials, semantic assertions, no brittle data    |

**Review skills** — run automatically after implementation (see [Post-Implementation Reviews](#post-implementation-reviews)):

| Skill        | Canonical checks                                                   |
| ------------ | ------------------------------------------------------------------ |
| `sdk-review` | Spec conformance, .NET/Python parity, breaking changes, test strength (runs the unit-test self-review) |
