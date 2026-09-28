---
name: sdk-review
description: "Reviews changed SDK files for spec conformance, .NET/Python parity, breaking-change marking, generated-code hygiene and test coverage. Use after implementing any change under dotnet/ or python/, before opening or updating a PR, or when asked to review an SDK change."
compatibility: Requires file system read access and git; network access to the public OpenAPI specs for spec checks.
metadata:
    author: api-sdk
    version: "1.0"
    category: quality-assurance
    keywords: review, sdk, parity, breaking-change, openapi, tests
---

## When to invoke this skill

- After any change under `dotnet/` or `python/` (post-implementation review)
- Before opening or updating an SDK PR

## Review Steps

1. **Scope** — `git diff origin/main...HEAD --stat`; group files by SDK.
2. **Checks** — run the unit-test self-review script, then apply each table below to the diff.
3. **Report** — see [Report format](#report-format).

### Spec conformance

| Check                                                              | Severity |
| ------------------------------------------------------------------ | -------- |
| Param/field name, type, enum values differ from the OpenAPI spec   | BLOCKING |
| Required/nullable differs from spec                                | WARNING  |
| Timestamp not sent as UTC ISO 8601 (`Z`)                           | BLOCKING |
| Empty query param sent when unset (`include=`, bare `?`)           | WARNING  |

### Parity

| Check                                                              | Severity |
| ------------------------------------------------------------------ | -------- |
| API change in one SDK only, no deferral ticket in PR body          | WARNING  |
| Same option named/typed differently across SDKs without reason     | SUGGESTION |

### Breaking changes

| Check                                                              | Severity |
| ------------------------------------------------------------------ | -------- |
| Breaking change (see [references/breaking-changes.md](references/breaking-changes.md)) not marked per [release conventions](../../instructions/release.instructions.md#versioning) | BLOCKING |
| Non-breaking PR marked as breaking                                 | WARNING  |
| Breaking change without migration note in PR body                  | WARNING  |
| Version placeholder `0.0.0` changed                                | BLOCKING |

### Generated code and tests

| Check                                                              | Severity |
| ------------------------------------------------------------------ | -------- |
| Hand edit in `python/heimdall_api_client/*_api_client/`            | BLOCKING |
| Findings from `bash .github/skills/sdk-write-unit-tests/scripts/self-review.sh origin/main`, checks 1 and 3 (no request assertion, untested new field) | BLOCKING |
| Optional query param without an omitted-when-unset test            | BLOCKING |
| Self-review check 2: changed test with only weak assertions        | WARNING  |
| Self-review check 4: new Python method missing from test lists     | WARNING  |
| Scenario in one SDK's tests but not the other's                    | WARNING  |
| Integration test with only weak assertions or a hard-coded production id (see `sdk-write-integration-tests`) | SUGGESTION |
| Unit test missing `[Trait("Category", "Unit")]` (.NET)             | BLOCKING |
| Public member without XML doc / docstring                          | SUGGESTION |

## Report format

| Severity   | Meaning                                                  |
| ---------- | -------------------------------------------------------- |
| BLOCKING   | Fix before merge: test failure, bug, wrong wire format   |
| WARNING    | Likely unintended or fragile; needs human review         |
| SUGGESTION | Safer or cleaner alternative exists                      |

- One section per check table; "No violations" when clean.
- Per finding: file, line, issue, concrete fix.
- End with `[N] BLOCKING  [N] WARNING  [N] SUGGESTION`.

## Validation

- Every changed file assessed; report ends with the summary line.
