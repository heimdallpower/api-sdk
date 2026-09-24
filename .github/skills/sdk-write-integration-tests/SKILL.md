---
name: sdk-write-integration-tests
description: "Write, strengthen and run .NET and Python SDK integration tests against the live External API, validating data shape and semantics instead of just a 200, without brittle production-data assumptions or leaked secrets. Use when adding integration coverage for a new endpoint, parameter or field, running the integration tests locally, debugging integration-test authentication failures, or reviewing integration tests for weak assertions."
compatibility: Requires .NET 10 SDK, Python 3.11 + Poetry, API client credentials, network access to the production API.
metadata:
    author: api-sdk
    version: "1.0"
    category: code-generation
    keywords: integration tests, live api, xunit, pytest, credentials, semantics
---

## Purpose

Integration tests hit the **production** API with a real client. A 200 or a non-empty list proves wiring only; the value is in checking that the data is shaped and behaves as the spec says. The repo is public — nothing identifying may leak.

| Flavor                        | .NET                                                                 | Python                                               |
| ----------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------- |
| One call, many assertions     | `IClassFixture<Scenario>`; `Scenario : AuthenticatedHeimdallApiClient` makes the call once | session fixtures in `conftest.py` (`api_client`, `line_id`, `facility_id`, `window`) |
| Many endpoints, same contract | one class per endpoint under `WhenAuthenticated/`                    | `@pytest.mark.parametrize("method_name", …)`         |
| Cross-endpoint consistency    | e.g. `AllSpanPhaseAndMeasurementPointIdsShouldExistInAssets`         | resolve ids via `get_assets()` in the test           |

## Workflow

### Step 1 — Get credentials

Integration tests require API client credentials in `HEIMDALL_CLIENT_ID` / `HEIMDALL_CLIENT_SECRET` (contact Heimdall Power for API access). Check tools and variables with `./scripts/check-prerequisites.sh` (or `.ps1`). Stale values from a shell profile override fresh ones — check which are set before debugging.

### Step 2 — Discover data, don't hard-code it

- Resolve line/facility/span ids from `GetAssetsAsync()` / `get_assets()` — `conftest.py` `line_id` is the pattern.
- Data may legitimately be empty (no sensor data in the window). Python: `pytest.skip("<reason>")`. .NET (xunit 2, no runtime skip): assert invariants that hold for empty results (`Assert.All`), and only require non-empty where the contract guarantees it.
- 404 means "no data" for this asset — skip with the reason (see `assert_endpoint_responds`), never pass silently.

### Step 3 — Write semantic assertions

See [references/checks.md](references/checks.md). Minimum per endpoint: ids are non-empty GUIDs · timestamps UTC and inside the requested window, or at/after `since` · units match `unit_system` · `include`-gated fields `null` unless requested, populated when requested · every referenced span/span phase/measurement point exists in the assets hierarchy · numeric ranges plausible.

### Step 4 — Self-review (run the checks, don't just recall the rules)

Tests passing doesn't prove this step happened:

```bash
python3 .github/skills/sdk-write-unit-tests/scripts/find-weak-tests.py dotnet/tests/integration python/tests/integration
grep -rnE 'Guid\.Parse\("[0-9a-f-]{36}"\)|UUID\("[0-9a-f-]{36}"\)' dotnet/tests/integration python/tests/integration
grep -rnE 'Console\.Write|ITestOutputHelper|print\(|logging\.' dotnet/tests/integration python/tests/integration
```

| # | Finding                                   | Fix                                                                 |
| - | ----------------------------------------- | ------------------------------------------------------------------- |
| 1 | Test with only weak assertions            | Add a semantic assertion from Step 3, or merge into a test that has one |
| 2 | Hard-coded production id                  | Discover it from assets; if kept, justify (e.g. a dedicated test line) |
| 3 | Output that could carry tokens, secrets, account or customer names | Remove; assert messages may name ids and endpoints only |

Delegating to a subagent doesn't skip this — run it against its diff yourself.

## Validation

1. .NET single test: `cd dotnet && dotnet test --filter "Category=Integration&FullyQualifiedName~GetCurrents"`; all: `--filter Category=Integration`.
2. Python single test: `cd python && poetry run pytest -m integration "tests/integration/test_when_fetching_latest_data.py::test_should_return_latest_line_data" -v`; all: `poetry run pytest -m integration`.
3. CI: `dotnet-integration-tests.yml` / `python-integration-tests.yml` run on push to `main` (and manual dispatch) with the repo secrets `HEIMDALL_CLIENT_ID` / `HEIMDALL_CLIENT_SECRET`. They run **after** merge: a failure turns `main` red but blocks nothing — check the run after merging.

## Gotchas

- `Failed to acquire access token` in every test → the credentials are wrong or stale, not the SDK; verify the variables before changing code.
- `ResultShouldIncludeMeasurementPoints` (`Assert.NotEmpty` on production assets) breaks if the test client loses measurement points — prefer invariants on whatever is returned.
- Several .NET suites hard-code one line id; a decommissioned line fails them all at once.
- `poetry run pytest` without a path also collects `tests/integration`; use `tests/unit` for unit runs.
- Never paste test output into PRs or issues without checking it for tokens, authentication error details and customer identifiers.
