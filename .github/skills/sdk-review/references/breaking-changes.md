# Breaking-change classification

## .NET

| Change                                                    | Breaking? | Why                                   |
| --------------------------------------------------------- | --------- | ------------------------------------- |
| New optional param **before** `cancellationToken`         | Yes       | Positional token calls stop compiling |
| New member on `IHeimdallApiClient`                        | Yes       | Custom implementations/mocks break    |
| New `required` property on a DTO                          | Yes       | Object initializers break             |
| Renamed/removed method, param, DTO, or property           | Yes       | Source + binary break                 |
| Changed property type or nullability (e.g. `T` → `T?`)    | Yes       | Callers must handle null              |
| New optional DTO property, new DTO, new enum              | No        | Additive                              |
| Bug fix in wire format (e.g. timestamp format)            | No (`fix`) | Callers unchanged                    |

Non-breaking alternative: a new overload instead of a new optional param. Decide with the user; the existing SDK style accepts the break and documents it.

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

PRs are squash-merged: the PR title and body become the commit on `main`.

- PR title: `feat(dotnet)!: add since to latest endpoints`
- PR body: *Release notes* → Breaking changes + Migration (before → after snippet, e.g. pass `cancellationToken: ct` by name).
- Last line of the PR body: `BREAKING CHANGE: <old signature> → <new signature>; <migration>`
