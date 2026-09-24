---
applyTo: "python/**"
---

# Python SDK — Conventions

Conventions only. For the workflow of adding API changes, see *Updating the SDK for API changes* in `CONTRIBUTING.md`.

## Three layers per endpoint

| Layer          | Path (under `python/heimdall_api_client/`)                 | Written by                   |
| -------------- | ---------------------------------------------------------- | ---------------------------- |
| Generated      | `{assets,capacity_monitoring,grid_insights}_api_client/`   | `openapi-python-client` only |
| Module wrapper | `assets.py`, `capacity_monitoring.py`, `grid_insights.py`  | Hand — one function per operation |
| Public client  | `client.py` → `HeimdallApiClient` methods                  | Hand — what users call       |

## Regenerating a module

```bash
cd python/scripts
pwsh ./generate-module-client.ps1 -Module grid_insights   # assets | capacity_monitoring | grid_insights
```

- Requires PowerShell 7 (`pwsh`) and Python; the script pins `openapi-python-client` and installs it.
- Downloads the spec from `https://external-api.heimdallcloud.com/openapi/{module}/v1/openapi.yaml` — the **deployed** API.
- Formats via `post_hooks` in `openapi_python_client_config.yaml`; aborts if output is unformatted.
- Commit the whole regenerated module; a diff limited to changed endpoints/models is the expected result.

## Rules

| Rule                                                                  | Why                                          |
| --------------------------------------------------------------------- | -------------------------------------------- |
| Never hand-edit `*_api_client/` (excluded from ruff)                  | Next regeneration wipes it                   |
| Wrapper: call `sync_detailed`, raise `HeimdallApiError` on non-200 with `body_preview` | Consistent errors across endpoints |
| Wrapper: `None` → `UNSET`; datetimes through `as_zulu`                 | Unset params omitted; UTC `Z` timestamps     |
| Enum params accept `Enum \| str`; convert with the enum constructor    | Invalid values fail before any request       |
| Client method: lazy-import the wrapper, wrap in `_execute_with_retry` | Existing pattern; retry and auth in one place |
| New params: optional keyword args appended **last**                   | Positional callers keep working              |
| Keep existing public names, even misspelled ones                      | Renaming is breaking                         |
| Docstring on every client method, meaning taken from the spec         | Primary user documentation                   |

## Tests

| Kind        | Location              | Pattern                                                                  |
| ----------- | --------------------- | ------------------------------------------------------------------------ |
| Unit        | `tests/unit/`         | Drive `HeimdallApiClient` over the recording transport in `_fake_transport.py`; assert query params and parsed models |
| Wrapper guard | `tests/unit/test_endpoint_wrappers_resolve.py` | Add every new wrapper and client method to its lists |
| Integration | `tests/integration/` (`@pytest.mark.integration`) | Real API, needs credentials; runs on `main` |

CI: `poetry check`, `poetry lock` sync check, `ruff check .`, `ruff format --check .`, `pytest tests/unit -v`, `poetry build`.

Writing tests: `sdk-write-unit-tests` and `sdk-write-integration-tests` skills. Bare `pytest` also collects `tests/integration`.
