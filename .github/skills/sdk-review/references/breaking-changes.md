# Breaking-change classification

## .NET

| Change                                                    | Breaking? | Why                                   |
| --------------------------------------------------------- | --------- | ------------------------------------- |
| New or reordered positional param on a client method      | Yes       | Positional calls stop compiling       |
| New `required` property or positional ctor on an options record | Yes | `new() { … }` call sites break        |
| New member on `IHeimdallApiClient`                        | Yes       | Custom implementations/mocks break    |
| New `required` property on a DTO                          | Yes       | Object initializers break             |
| Renamed/removed method, param, DTO, or property           | Yes       | Source + binary break                 |
| Changed property type or nullability (e.g. `T` → `T?`)    | Yes       | Callers must handle null              |
| Changed return or collection type (e.g. `List<T>` → `IReadOnlyList<T>`) | Yes | Code using the old type stops compiling |
| Public type or member made `internal`                     | Yes       | Same as removal                       |
| New optional DTO property, new DTO, new enum              | No        | Additive                              |
| New optional `init` property on an options record         | No        | Additive; how optional query params are added |
| Bug fix in wire format (e.g. timestamp format)            | No (`fix`) | Callers unchanged                    |

New optional query params go on the method's options record (e.g. `GetLatestCurrentOptions`), which is non-breaking.

## Python

| Change                                                    | Breaking? | Why                                   |
| --------------------------------------------------------- | --------- | ------------------------------------- |
| New optional kwarg appended last                          | No        | Positional callers unaffected         |
| New kwarg inserted before existing ones                   | Yes       | Positional callers shift              |
| Renamed/removed client method, wrapper, or kwarg          | Yes       | Imports/calls fail                    |
| Generated model gains a required field                    | Yes       | Hand construction fails; positional args shift into the wrong field |
| Generated model/enum renamed by the spec                  | Yes       | Imports fail                          |

## API-side changes

| Spec change                          | SDK impact                                             |
| ------------------------------------ | ------------------------------------------------------ |
| Removed endpoint/param/field         | Breaking in both SDKs — confirm with the user first    |
| Default changed (e.g. `since` window)| Behavioral; call out in release notes even if no code change |
| New required query param             | Breaking in both SDKs                                  |

## Also check

| Check                                                     | Why                                   |
| --------------------------------------------------------- | ------------------------------------- |
| Regenerated attrs model field order vs. hand-built fixtures/examples | Positional construction silently misassigns |
| Files are UTF-8 without BOM (`.editorconfig` `charset = utf-8`) | Generators and editors sometimes add a BOM |

## Marking

`!` in the PR title and a closing `BREAKING CHANGE:` line — see the [release conventions](../../../instructions/release.instructions.md#versioning). Migration note: before → after snippet (e.g. `GetLatestHeimdallDlrAsync(id, Quantity.ApparentPower)` → `GetLatestHeimdallDlrAsync(id, new() { Quantity = Quantity.ApparentPower })`).
