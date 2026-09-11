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

# Path sets: the SDK directory PLUS its build/publish workflows — a workflow
# edit can change what ships in the package without touching the SDK directory.
paths_for() {
  case "$1" in
    dotnet) printf '%s\n' dotnet .github/workflows/nuget-publish.yml '.github/workflows/dotnet-*.yml' ;;
    python) printf '%s\n' python .github/workflows/python-publish.yml '.github/workflows/python-*.yml' ;;
  esac
}
mapfile -t paths       < <(paths_for "$sdk")
mapfile -t other_paths < <(paths_for "$other")

# Highest stable tag with this SDK's prefix, ranked by SEMVER VALUE — not by
# `git describe`, which only sees tags reachable from HEAD and so can propose
# a version that already exists. Falls back to the legacy v* tags until the
# first prefixed tag is cut. `|| true` keeps an empty match from tripping
# pipefail, so the explicit error below is what the caller sees.
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

# Suggested bump from conventional-commit types on the SUBJECT line.
# ADVISORY ONLY: it reads what people wrote, not what they did — a breaking
# change typed `chore:` looks like "none" here. A human decides.
suggest_bump() {
  local level=0 line
  # Regexes live in variables: bash's [[ =~ ]] parser chokes on an inline
  # pattern with a `(...)` group before the regex is ever evaluated.
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

# "BREAKING CHANGE" is a footer: it must start its own line. A substring
# match would also fire on changelogs quoted inside a dependabot body.
has_breaking_footer() {
  grep -qE '^BREAKING[ -]CHANGE:' <<< "$1"
}

# The type comes from subjects only — a dependabot body embeds the upstream
# project's own feat:/fix: lines, which are not our changes. Bodies are read
# only for a line-anchored breaking footer.
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
tag=${version:+$sdk-v$version}

list() { if [[ -n "$1" ]]; then printf '%s\n' "$1" | sed 's/^/- /'; else echo "_none_"; fi; }
report() {
  echo "## prepare-release: $sdk"
  echo "- Package: \`$package\`"
  echo "- Baseline: \`$base\` → target \`${head_sha:0:7}\`"
  echo "- Suggested bump: **$suggested**${override:+ (overridden to \`$override\`)}"
  echo "- Proposed tag: \`${tag:-none}\`"
  echo; echo "### $sdk changes since $base"; list "$changes"
  echo; echo "### Commits also touching files outside both SDK path sets (review)"; list "$outside"
  echo; echo "### ⚠ Unreleased on $other since $other_base"; list "$other_changes"
}
report
if [[ -n "${GITHUB_STEP_SUMMARY:-}" ]]; then report >> "$GITHUB_STEP_SUMMARY"; fi

if [[ -z "$version" ]]; then
  echo "::notice::Nothing to release for $sdk: no feat/fix/breaking commits since $base. Pass a version override to force a release."
  exit 0
fi

# An override can force a release with zero matching commits. That's its
# purpose, but burning a registry version on an empty changelog should be loud.
if [[ -z "$changes" ]]; then
  echo "::warning::No changes detected in $sdk since $base — drafting $tag anyway (version override given)."
fi

# Same guard the publish workflow uses; set -e aborts here on an invalid tag.
# GITHUB_OUTPUT=/dev/null discards its key-value lines, which we don't use.
GITHUB_OUTPUT=/dev/null bash "$here/tag-guard.sh" "$sdk" "$tag" 1>&2

# Refuse to reuse a tag: `gh release create` on an existing tag succeeds but
# ignores --target, so the draft would ship whatever that tag already points at.
if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
  echo "::error::Tag $tag already exists — refusing to draft a release that would reuse a published version."
  exit 1
fi

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
  # Compares against the target SHA: the tag doesn't exist until the draft
  # is published, so a $tag-based link would 404 during review.
  echo "**Full changelog:** https://github.com/heimdallpower/api-sdk/compare/$base...$head_sha"
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
