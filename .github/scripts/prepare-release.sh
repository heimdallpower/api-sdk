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

# Last stable tag with this SDK's prefix (prereleases excluded so a -beta.1 is
# never the baseline). Before the first prefixed tag exists, fall back to the
# highest legacy v* tag (v4.0.0 today). sed -n 1p, not head -1: head can close
# the pipe early and trip pipefail.
last_tag_for() {
  git describe --tags --abbrev=0 --match "$1-v*" --exclude "$1-v*-*" 2>/dev/null \
    || git tag --list 'v*' --sort=-v:refname | grep -v -- '-' | sed -n 1p
}
base=$(last_tag_for "$sdk")
other_base=$(last_tag_for "$other")
head_sha=$(git rev-parse HEAD)

changes=$(git log "$base..HEAD" --format='%h %s' -- "${paths[@]}")
other_changes=$(git log "$other_base..HEAD" --format='%h %s' -- "${other_paths[@]}")
outside=$(git log "$base..HEAD" --format='%h %s' -- . ':!dotnet' ':!python' \
  ':!.github/workflows/*publish.yml' ':!.github/workflows/dotnet-*.yml' ':!.github/workflows/python-*.yml')

# Suggested bump from conventional-commit types. ADVISORY ONLY: it reads what
# people wrote, not what they did — the .NET 10 upgrade (8e518a0) was typed
# `chore:` and dropped net9.0 consumers; this says "none" for it. A human decides.
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
    if [[ "$line" =~ $breaking_re ]] || [[ "$line" == *"BREAKING CHANGE"* ]]; then level=3
    elif [[ "$line" =~ $feat_re ]] && (( level < 2 )); then level=2
    elif [[ "$line" =~ $fix_re ]] && (( level < 1 )); then level=1
    fi
  done
  case $level in 3) echo major ;; 2) echo minor ;; 1) echo patch ;; *) echo none ;; esac
}
suggested=$(git log "$base..HEAD" --format='%s%n%b' -- "${paths[@]}" | suggest_bump)

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

# Same guard the publish workflow uses. Its ::notice/::error lines go to stderr
# so they stay visible; set -e aborts this script when it exits 1.
GITHUB_OUTPUT=/dev/null bash "$here/tag-guard.sh" "$sdk" "$tag" 1>&2

notes=$(mktemp)
{
  echo "## $package $version"; echo
  list "$changes"; echo
  echo "**Full changelog:** https://github.com/heimdallpower/api-sdk/compare/$base...$tag"
} > "$notes"

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
rm -f "$notes"
