# SDK Unit Test Checks

## Scenarios per change

| Change                     | Required scenarios (both SDKs)                                                        |
| -------------------------- | ------------------------------------------------------------------------------------- |
| New optional query param   | Sent with exact value · omitted when unset · combined with existing params            |
| New enum param             | Enum and string variants (Python) · every enum member's wire value · invalid rejected, zero requests |
| New timestamp param        | Non-UTC input → `…Z` output; .NET `ToApiTimestamp` format `yyyy-MM-ddTHH:mm:ss.fffffffZ`, Python `as_zulu` |
| `unit_system`              | `metric` and `imperial` on the wire; response parsed for both units                   |
| New response field         | Parsed value asserted; `null` from the API → `null`/`None`; absent-vs-empty list distinguished |
| `include`-gated field      | `null` when not requested · populated and fully asserted when requested               |
| New endpoint               | Exact path · all params · full response parse · 404 path via `HeimdallApiException`/`HeimdallApiError` |
| New Python client method   | Added to `test_endpoint_wrappers_resolve.py`; kwargs guarded by the signature test     |

## Non-discriminating tests

A test that passes under both the correct and an obviously buggy implementation isn't testing anything.

| Failure mode                                                   | Fix                                                                 |
| -------------------------------------------------------------- | ------------------------------------------------------------------- |
| Asserts the call returned / is not null                        | Assert every new field's value                                      |
| Asserts a param is present, not its value                      | `Assert.Equal(expected, query["k"])`                               |
| Timestamp input already UTC                                    | Use a `+01:00` input so a missing conversion fails                  |
| Only the "set" case tested                                     | Add omitted-when-unset — catches `include=` / bare `?` regressions  |
| Invalid value test only checks the exception                   | Also assert zero requests were sent                                 |
| JSON where every field has the same value (`1.0`, same GUID)   | Distinct values per field, so a swapped mapping fails               |
| `include` test JSON always contains the breakdown              | Separate bodies for requested / not requested                       |
| Scenario exists in one SDK only                                | Mirror it in the other SDK, or state why in the PR                  |
| Positional-argument change not guarded (Python)                | Extend the `inspect.signature` guard with the new parameter         |
| Generated model fixture built positionally                     | Build with keywords or from JSON (`from_dict`) — new required fields shift positions |

## Test data

- Take bodies from the spec `example:` blocks or captured responses; replace ids with fixed fake GUIDs and remove customer or line names.
- Keep `snake_case` keys exactly as the API sends them.
- Files are UTF-8 without BOM (`.editorconfig`).
