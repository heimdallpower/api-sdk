#!/usr/bin/env bash
# Draft a GitHub Release for ONE SDK from path-filtered history. Never publishes.
#
# Usage: prepare-release.sh <dotnet|python> [version]
#   version   optional override, e.g. 4.1.0 or 4.1.0-rc.1 (validated with tag-guard.sh)
# Env:
#   DRY_RUN=1              print the `gh release create` command instead of running it
#   GH_TOKEN               required unless DRY_RUN=1 (workflow passes github.token)
#   GITHUB_STEP_SUMMARY    if set, the report is appended there
#
# Requires a full clone with tags (actions/checkout: fetch-depth: 0, fetch-tags: true).
set -euo pipefail

sdk=${1:-}
override=${2:-}
here="$(cd "$(dirname "$0")" && pwd)"
cd "$(git rev-parse --show-toplevel)"

case "$sdk" in
  dotnet) other=python; package="HeimdallPower.Api.Client (+ .Extensions)" ;;
  python) other=dotnet; package="heimdallpower-api-client" ;;
  *) echo "::error::unknown sdk '$sdk' (expected dotnet or python)"; exit 2 ;;
esac

# Path sets: the SDK directory PLUS its build/publish workflows. dcbefed (#151)
# changed what ships in the .nupkg by editing only nuget-publish.yml and
# python/pyproject.toml — a bare `-- dotnet/` filter would file it under Python.
paths_for() {
  case "$1" in
    dotnet) printf '%s\n' dotnet .github/workflows/nuget-publish.yml '.github/workflows/dotnet-*.yml' ;;
    python) printf '%s\n' python .github/workflows/python-publish.yml '.github/workflows/python-*.yml' ;;
  esac
}
mapfile -t paths       < <(paths_for "$sdk")
mapfile -t other_paths < <(paths_for "$other")

# Last stable tag with this SDK's prefix, ranked by SEMVER VALUE, not git
# ancestry. `git describe --tags --abbrev=0` returns the nearest tag reachable
# from HEAD — a release cut on a branch that isn't an ancestor of the dispatch
# ref is invisible to it, so the baseline can be stale and the proposed tag
# can collide with one that already exists. `git tag --list ... --sort=-v:refname`
# ranks every tag matching the prefix by version, independent of reachability.
# Before the first prefixed tag exists, fall back to the highest legacy v*
# tag (v4.0.0 today) — same sort strategy on both branches, on purpose.
#
# Stable tags are matched with an ANCHORED regex (^prefix-vX.Y.Z$ / ^vX.Y.Z$),
# not `grep -v -- '-'`: every "$prefix-v*" tag already contains a mandatory
# dash between the prefix and "v" (e.g. "dotnet-v4.1.0"), so `grep -v -- '-'`
# would exclude ALL of them, prefixed stable tags included, and always fall
# through to the legacy branch. Verified against a scratch repo with
# dotnet-v4.1.0/dotnet-v4.2.0 tags: `grep -v -- '-'` returned nothing for
# either. The anchored-regex form correctly keeps only "no prerelease
# suffix" tags on both branches.
#
# Each `... || true` neutralizes pipefail on an empty match (no tags yet) so
# this function can fail LOUDLY of its own accord below, instead of silently
# killing the caller via set -e with no output.
last_tag_for() {
  local prefix=$1 tag
  tag=$(git tag --list "${prefix}-v*" --sort=-v:refname | grep -E "^${prefix}-v[0-9]+\.[0-9]+\.[0-9]+\$" | sed -n 1p || true)
  if [[ -z "$tag" ]]; then
    tag=$(git tag --list 'v*' --sort=-v:refname | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sed -n 1p || true)
  fi
  if [[ -z "$tag" ]]; then
    echo "::error::no baseline tag found for $prefix" >&2
    return 1
  fi
  printf '%s\n' "$tag"
}
base=$(last_tag_for "$sdk")
other_base=$(last_tag_for "$other")
head_sha=$(git rev-parse HEAD)

changes=$(git log "$base..HEAD" --format='%h %s' -- "${paths[@]}")
other_changes=$(git log "$other_base..HEAD" --format='%h %s' -- "${other_paths[@]}")
outside=$(git log "$base..HEAD" --format='%h %s' -- . ':!dotnet' ':!python' \
  ':!.github/workflows/*publish.yml' ':!.github/workflows/dotnet-*.yml' ':!.github/workflows/python-*.yml')

# Suggested bump from conventional-commit types, read from the SUBJECT line
# only. ADVISORY ONLY: it reads what people wrote, not what they did — the
# .NET 10 upgrade (8e518a0) was typed `chore:` and dropped net9.0 consumers;
# this says "none" for it. A human decides.
suggest_bump() {
  local level=0 line
  # Regexes are held in variables, not written inline in the [[ =~ ]] test:
  # bash's conditional-expression parser cannot reliably tokenize an unquoted
  # pattern containing a `(...)` group that itself ends in `)?!` — it raises
  # "syntax error in conditional expression: unexpected token `)'" before the
  # regex is ever evaluated. Routing through a variable (as tag-guard.sh
  # already does for its own regex) sidesteps the parser, not the semantics.
  local breaking_re='^[a-z]+(\([^)]*\))?!:'
  local feat_re='^feat(\([^)]*\))?:'
  local fix_re='^fix(\([^)]*\))?:'
  while IFS= read -r line; do
    if [[ "$line" =~ $breaking_re ]]; then level=3
    elif [[ "$line" =~ $feat_re ]] && (( level < 2 )); then level=2
    elif [[ "$line" =~ $fix_re ]] && (( level < 1 )); then level=1
    fi
  done
  case $level in 3) echo major ;; 2) echo minor ;; 1) echo patch ;; *) echo none ;; esac
}

# Per Conventional Commits, "BREAKING CHANGE" is a FOOTER: it must start its
# own line ("BREAKING CHANGE:" or "BREAKING-CHANGE:"), not merely appear as a
# substring anywhere in the message. A whole-body substring match would also
# fire on other projects' conventional-commit text embedded in a dependency
# bump's body (e.g. dependabot inlining an upstream changelog) — see
# resolve_bump below.
has_breaking_footer() {
  grep -qE '^BREAKING[ -]CHANGE:' <<< "$1"
}

# Combines the two signals while keeping them separate on purpose: the TYPE
# (feat/fix/!) comes only from subject lines, never from a commit's body —
# a dependabot bump's body routinely embeds the *upstream* project's own
# `feat:`/`fix:` changelog lines, which are not our changes and must not be
# read as such. The breaking-footer check runs over bodies but only as a
# line-anchored footer, not a substring search (see has_breaking_footer).
resolve_bump() {
  local subjects=$1 bodies=$2 level
  level=$(printf '%s\n' "$subjects" | suggest_bump)
  if [[ "$level" != "major" ]] && has_breaking_footer "$bodies"; then
    level=major
  fi
  printf '%s\n' "$level"
}
subjects=$(git log "$base..HEAD" --format='%s' -- "${paths[@]}")
bodies=$(git log "$base..HEAD" --format='%b' -- "${paths[@]}")
suggested=$(resolve_bump "$subjects" "$bodies")

base_version=${base#"$sdk-v"}; base_version=${base_version#v}
IFS=. read -r maj min pat <<< "$base_version"
case "$suggested" in
  major) next="$((maj + 1)).0.0" ;;
  minor) next="$maj.$((min + 1)).0" ;;
  patch) next="$maj.$min.$((pat + 1))" ;;
  *)     next="" ;;
esac
version=${override:-$next}
tag="$sdk-v$version"

list() { if [[ -n "$1" ]]; then printf '%s\n' "$1" | sed 's/^/- /'; else echo "_none_"; fi; }
report() {
  echo "## prepare-release: $sdk"
  echo "- Package: \`$package\`"
  echo "- Baseline: \`$base\` → target \`${head_sha:0:7}\`"
  echo "- Suggested bump: **$suggested**${override:+ (overridden to \`$override\`)}"
  echo "- Proposed tag: \`${version:+$tag}\`"
  echo; echo "### $sdk changes since $base"; list "$changes"
  echo; echo "### Commits touching files outside both SDK path sets (review)"; list "$outside"
  echo; echo "### ⚠ Unreleased on $other since $other_base"; list "$other_changes"
}
report
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then report >> "$GITHUB_STEP_SUMMARY"; fi

if [[ -z "$version" ]]; then
  echo "::notice::Nothing to release for $sdk: no feat/fix/breaking commits since $base. Pass a version override to force a release."
  exit 0
fi

# An override can force a release even with zero matching commits. That's
# the override's purpose, but a burned registry version with an empty
# changelog is a foot-gun done silently — make it loud instead.
if [[ -z "$changes" ]]; then
  echo "::warning::No changes detected in $sdk since $base — drafting $tag anyway (version override given)."
fi

# Same guard the publish workflow uses. tag-guard.sh writes its own
# ::notice::/::error:: lines to stdout by default; redirecting that to this
# script's stderr just keeps the two streams separate — both still show up
# in the Action log either way, so this is not what makes them "visible".
# GITHUB_OUTPUT=/dev/null discards its publish=/version= key-value lines,
# which this caller doesn't use. set -e aborts this script when tag-guard.sh
# exits 1 (invalid tag for this sdk).
GITHUB_OUTPUT=/dev/null bash "$here/tag-guard.sh" "$sdk" "$tag" 1>&2

notes=$(mktemp)
trap 'rm -f "$notes"' EXIT
{
  echo "## $package $version"; echo
  if [[ -n "$changes" ]]; then
    list "$changes"
  else
    echo "No changes detected in $sdk since $base."
  fi
  echo
  # Compares against the target SHA, not the tag: the tag doesn't exist yet
  # (this draft hasn't been published), so a $tag-based link 404s during
  # exactly the review step this whole design exists for.
  echo "**Full changelog:** https://github.com/heimdallpower/api-sdk/compare/$base...$head_sha"
} > "$notes"

# Refuse to reuse a tag. Even with the version-sort baseline fix above, a tag
# can still exist with its release deleted: `gh release create` on an
# existing tag succeeds and GitHub will NOT move that tag, so --target is
# silently ignored and the draft ships whatever the old tag already points
# at instead of $head_sha.
if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
  echo "::error::Tag $tag already exists — refusing to draft a release that would reuse a published version."
  exit 1
fi

# --target pins the tag to THIS commit. Without it GitHub tags the default
# branch's HEAD at publish time, and anything merged in between ships silently.
cmd=(gh release create "$tag" --draft --target "$head_sha" --title "$tag" --notes-file "$notes")
if [[ "$version" == *-* ]]; then cmd+=(--prerelease); fi

if [[ "${DRY_RUN:-0}" == 1 ]]; then
  echo "DRY_RUN: ${cmd[*]}"; echo "--- notes ---"; cat "$notes"
else
  url=$("${cmd[@]}")
  echo "::notice::Draft created: $url — review, then publish."
  if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then printf '\n**Draft:** %s\n' "$url" >> "$GITHUB_STEP_SUMMARY"; fi
fi
