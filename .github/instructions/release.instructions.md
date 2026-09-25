---
applyTo: ".github/**"
---

# CI, Versioning and Release — Conventions

Human-facing release steps: `CONTRIBUTING.md` → *Cutting a release*. This file is the agent-facing summary.

## Workflows

| Workflow                         | Trigger                          | Runs                                                        |
| -------------------------------- | -------------------------------- | ----------------------------------------------------------- |
| `pr-validation.yml`              | Every PR (title edits too)       | Conventional Commits check on the **PR title**              |
| `dotnet-build-and-test.yml`      | PR/push touching `dotnet/**`     | restore, build, `dotnet test --filter Category=Unit`        |
| `python-build.yml`               | PR/push touching `python/**`     | `poetry check`, lock sync, ruff lint/format, unit tests, build |
| `dotnet-integration-tests.yml`, `python-integration-tests.yml` | PRs from this repo, push to `main`, manual | Integration tests with repo secrets |
| `release-scripts-test.yml`       | Changes to `.github/scripts/**` or publish workflows | `tag-guard.test.sh` + grep safety asserts |
| `prepare-release.yml`            | Manual, per SDK                  | `prepare-release.sh` → **draft** GitHub release             |
| `nuget-publish.yml`, `python-publish.yml` | Release published       | `tag-guard.sh` → pack/build with tag version → OIDC publish |

## Versioning

| Rule                                                              | Why                                             |
| ----------------------------------------------------------------- | ----------------------------------------------- |
| Version = tag only: `dotnet-vX.Y.Z[-pre]`, `python-vX.Y.Z[-(alpha\|beta\|rc).N]` | `0.0.0` placeholders are overridden in CI |
| Suggested bump comes from commit **subjects** since the last tag of that SDK | Type the commit honestly                  |
| Squash merge: commit on `main` = PR title + PR body               | Branch-commit messages never reach `main`       |
| `!` in the PR title, or a body line starting `BREAKING CHANGE:` → major | Otherwise a breaking change ships as minor |
| `feat` → minor, `fix` → patch, others → no release                | `docs`/`chore`/`test` alone draft nothing       |
| Several PRs → one release per SDK; tag after the last one merges  | Avoid burning versions mid-series               |
| Never delete a tag or reuse a version                             | Registries reject reuse; tags record burned versions |

## Changelog

- No `CHANGELOG.md`; the changelog is the GitHub release for each tag (`pyproject.toml` links to Releases).
- `prepare-release.sh` lists commit subjects since the last tag — write subjects as release notes.
- Fill the optional *Release notes* section of the PR template (Breaking changes / Migration / Added / Fixed); it becomes the squash-commit body and the releaser pastes it into the draft.
- Breaking PR: end the body with `BREAKING CHANGE: <summary>`. Never start a line with that phrase in a non-breaking body — `prepare-release.sh` would suggest a major.
- Don't click *Generate release notes* — it compares against the other SDK's release.

## Rules for agents

- Don't create tags, publish releases, or dispatch `prepare-release.yml`.
- Changes to `tag-guard.sh`, `prepare-release.sh` or `*publish.yml` need explicit user approval and must keep `release-scripts-test.yml` green.
- Shell scripts stay LF (`.gitattributes`); YAML uses 2-space indent; all files UTF-8 without BOM (`.editorconfig`).
