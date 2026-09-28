# SDK Integration Test Checks

## Semantic assertions

| Aspect            | Assert                                                                                   |
| ----------------- | ---------------------------------------------------------------------------------------- |
| Ids               | Not `Guid.Empty` / valid `UUID`; referenced span, span phase, measurement point ids exist in `GetAssets` |
| Timestamps        | Offset zero (UTC) · within `[from, to]` for windowed calls · `>= since` for latest calls  |
| `since`           | A generous `since` returns data; a `since` newer than all data gives 404 (no data), not stale data |
| Units             | `unit` matches `unit_system` (metric vs imperial) and `quantity` (`Ampere` vs `MVA`); metric unchanged |
| `apparent_power`  | MVA = √3 · V · A / 10⁶ for the same calculation; V = operational voltage if > 0, else nominal |
| Paired calls      | Refetch until both carry the same timestamp / `updated_timestamp` before comparing |
| `include`         | Breakdown `null` when not requested; non-null and consistent with the aggregate when requested |
| Aggregates        | `min <= max`; `max_at_span_id` / `min_at_span_id` point to spans on the requested line    |
| Ordering          | Sequences ordered as the spec states (e.g. transient ratings by duration)                 |
| Types             | Enum-like strings within the spec's enum values                                          |

## Brittleness

| Failure mode                                            | Fix                                                        |
| ------------------------------------------------------- | ---------------------------------------------------------- |
| `Assert.NotEmpty` on data that can legitimately be empty | Invariants over the returned items; Python: skip with reason |
| Hard-coded asset id                                     | Discover from assets; keep a fixed id only for a dedicated test asset, with a comment |
| Fixed historical window with no guarantee of data       | Relative window (`now - 1 day`) or discover a window with data |
| 404 swallowed as pass                                   | Skip with reason (Python) or assert the documented 404     |
| Exact values from production                            | Ranges and relationships, not exact numbers                |

## Secrets and public-repo hygiene

- Credentials only via environment variables; never in code, fixtures, or assert messages.
- No logging of tokens, headers, account, customer or line names.
- Assert messages may contain ids and endpoint names only.
