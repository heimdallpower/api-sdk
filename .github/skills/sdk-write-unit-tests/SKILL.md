---
name: sdk-write-unit-tests
description: "Write or strengthen .NET and Python SDK unit tests that drive the real client over a fake HTTP transport, and self-review them with scripted checks before calling the work done. Use when adding tests for a new endpoint, query parameter, enum or response field, when asked to double-check or strengthen SDK unit test coverage, or when keeping .NET and Python tests in parity."
compatibility: Requires .NET 10 SDK, Python 3.11 + Poetry, bash and python3 for the self-review scripts.
metadata:
    author: api-sdk
    version: "1.0"
    category: code-generation
    keywords: unit tests, xunit, pytest, httpx, fake transport, query string, deserialization, parity
---

## Purpose

Unit tests call the **public client** end to end; only the HTTP transport is fake. A test that only proves "the call returned something" catches nothing — assert the request that went out and every field that came back.

| Under test                         | .NET                                                        | Python                                          |
| ---------------------------------- | ----------------------------------------------------------- | ----------------------------------------------- |
| Request (path, query) + parsing    | `Fakes/RecordingHttpMessageHandler` + `HeimdallApiClientFactory.Create(handler)`, `QueryString.Of(request)` | `_fake_transport.RecordingTransport(body)` + `make_client(transport)`, `transport.last_params` |
| Same scenario across many endpoints | `[Theory]` + `TheoryData` of `(name, json, call)` — see `WhenRequestingLatestValues/SinceParameter.cs` | `@pytest.mark.parametrize` over `_CASES` — see `test_quantity_on_latest_endpoints.py` |
| Error handling, retry, proxy       | `WhenHandlingErrorResponses/`, `WhenUsingResilienceExtensions/` | `test_retry_behavior.py`                        |
| Public signature compatibility     | Compiler + migration note (breaking by design)              | `inspect.signature` guard — `test_new_parameters_are_appended_as_optional_keywords` |
| Wrapper wiring                     | —                                                           | `test_endpoint_wrappers_resolve.py` lists       |

## Workflow

### Step 1 — Follow the existing pattern

- .NET: folder `When<Doing>/`, one class per method or concern, `[Trait("Category", "Unit")]`, JSON as raw string literals, fixed GUID constants.
- Python: `tests/unit/test_<feature>.py`, module docstring stating what is proven, `RecordingTransport` from `_fake_transport.py`.
- Same scenarios in both SDKs; name them alike so parity is reviewable.

### Step 2 — Decide the scenarios

Per new parameter or field — see [references/checks.md](references/checks.md) for the full list:
exact path + query when set · omitted when unset · invalid value rejected with **no request sent** · ISO 8601 `Z` timestamps from a non-UTC offset · enum and string variants · unit systems · null vs empty list · realistic JSON parsed field by field.

### Step 3 — Write strong assertions

- Request: `Assert.Equal("/grid_insights/v1/lines/{id}/currents/latest", uri.AbsolutePath)`; `transport.last_request.url.path == path`.
- Query value, not presence: `Assert.Equal("2026-01-01T12:30:00.0000000Z", query["since"])` from a `+01:00` input.
- Omitted: `Assert.Null(query["include"])`; `assert "include" not in transport.last_params`.
- Parsing: every new field with its expected value (`Assert.Collection`, `Assert.Single` then field asserts) — never `NotNull` alone.
- JSON bodies from the spec examples or anonymized real responses, `snake_case`, including `null` fields.

### Step 4 — Self-review (run the checks, don't just recall the rules)

Tests passing doesn't prove this step happened. From the repo root:

```bash
bash .github/skills/sdk-write-unit-tests/scripts/self-review.sh origin/main
```

| # | Check                                                        | Script basis                                        |
| - | ------------------------------------------------------------ | --------------------------------------------------- |
| 1 | Test file uses the fake transport but never asserts the request | `grep -L 'QueryString.Of\|AbsolutePath\|RequestUri'` / `'last_params\|url.path'` |
| 2 | Test whose only assertions are weak (`NotNull`, `NotEmpty`, `is not None`, status) | `scripts/find-weak-tests.py`   |
| 3 | Optional query param with no omitted-when-unset test         | `AddQueryParam("…")` keys vs. `Assert.Null(query["…"])` / `"…" not in` |
| 4 | New DTO property / model field never referenced in tests     | `git diff <base>` → `grep -w` in tests              |
| 5 | New Python client method missing from the test lists         | `git diff <base> -- client.py` → `grep` in tests    |

Delegating to a subagent doesn't skip this — run it against its diff yourself; "tests passed" isn't proof it self-reviewed. Every finding gets a fix or a stated reason. Then walk the failure-mode table in [references/checks.md](references/checks.md).

## Validation

1. .NET: `cd dotnet && dotnet test --filter "Category=Unit&FullyQualifiedName~<Class>"`, then the full `--filter Category=Unit`.
2. Python: `cd python && poetry run pytest tests/unit/<file>.py -v`, then `poetry run pytest tests/unit`, `ruff check .`, `ruff format --check .`.
3. Self-review script: no unexplained findings.

## Gotchas

- Check 4 matches by word: common names (`Id`, `Value`, `Timestamp`) always "pass" — verify those by hand.
- .NET sends `unit_system` and `quantity` with defaults on purpose; Python omits them. The script allows for that — don't "fix" either SDK to match.
- Python `make_client` bypasses auth by patching `_get_authenticated_client`; a test that needs real token behavior belongs in `test_auth_service.py`.
- An invalid-value test must assert the transport saw **zero** requests (`transport.requests == []`), not just that it raised.
- Deserialization tests with hand-trimmed JSON miss fields the API actually sends — start from the spec example.
