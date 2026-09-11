#!/usr/bin/env bash
# DRY_RUN smoke test for prepare-release.sh: pins the behaviours that carry a
# real guarantee — draft-only, target pinned to a real commit, no tag reuse,
# baseline by version value, prerelease flag.
#
# Runs against a throwaway fixture repo under mktemp, deleted on exit, with
# DRY_RUN=1 hardcoded on every call. It never touches this repo's tags or
# history and never shells out to the real `gh`.
#
# Run: bash .github/scripts/prepare-release.smoke.test.sh
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
fail=0

ok()  { echo "ok   $1"; }
bad() { echo "FAIL $1"; fail=1; }

fixture=$(mktemp -d "${TMPDIR:-/tmp}/prepare-release-smoke.XXXXXX")
cleanup() { rm -rf "$fixture"; }
trap cleanup EXIT

# --- build the fixture repo -------------------------------------------------
git init -q "$fixture"
git -C "$fixture" config user.email "smoke@example.invalid"
git -C "$fixture" config user.name "Smoke Test"
git -C "$fixture" config core.autocrlf false

mkdir -p "$fixture/.github/scripts" "$fixture/dotnet"
cp "$here/prepare-release.sh" "$fixture/.github/scripts/prepare-release.sh"
cp "$here/tag-guard.sh"       "$fixture/.github/scripts/tag-guard.sh"
chmod +x "$fixture/.github/scripts/"*.sh

commit() {
  echo "$RANDOM" >> "$fixture/dotnet/file.txt"
  git -C "$fixture" add dotnet/file.txt
  git -C "$fixture" commit -q -m "$1"
}

# Legacy-format tag so last_tag_for("python") has a fallback baseline; without
# it the script aborts before reaching the behaviour under test.
commit "chore: initial"
git -C "$fixture" tag v1.0.0
git -C "$fixture" tag dotnet-v4.9.0

# Tagged so a lexicographic sort would rank 4.9.0 above 4.10.0; only a
# semver-value sort picks 4.10.0.
commit "feat(dotnet): add widget"
git -C "$fixture" tag dotnet-v4.10.0

# A prerelease tag newer than the stable baseline is never the baseline.
commit "feat(dotnet): add gadget"
git -C "$fixture" tag dotnet-v4.11.0-beta.1

commit "fix(dotnet): correct widget bug"

run() {
  # DRY_RUN=1 is hardcoded: never exercise the real `gh release create`.
  ( cd "$fixture" && DRY_RUN=1 bash "$fixture/.github/scripts/prepare-release.sh" "$@" ) 2>&1
}

# --- baseline: chosen by version VALUE, not string/creation order ----------
out=$(run dotnet)
if grep -q 'Baseline: `dotnet-v4.10.0`' <<< "$out"; then
  ok "baseline picks highest semver VALUE (4.10.0 over 4.9.0), not string order"
else
  bad "baseline did not resolve to dotnet-v4.10.0"
  echo "$out"
fi

# --- baseline: a prerelease tag is never chosen as the stable baseline -----
if ! grep -q 'Baseline: `dotnet-v4.11.0-beta.1`' <<< "$out"; then
  ok "prerelease tag (4.11.0-beta.1) is not selected as baseline"
else
  bad "prerelease tag was selected as baseline"
fi

# --- DRY_RUN command shape: --draft and --target <40-hex sha> --------------
if grep -q -- '--draft' <<< "$out"; then
  ok "emitted command contains --draft"
else
  bad "emitted command is missing --draft"
fi

if grep -qE -- '--target [0-9a-f]{40}([[:space:]]|$)' <<< "$out"; then
  ok "emitted command contains --target followed by a 40-hex sha"
else
  bad "emitted command is missing a well-formed --target <sha>"
fi

# --- stable version: no --prerelease ----------------------------------------
if grep -q 'DRY_RUN: gh release create' <<< "$out" && ! grep -E 'DRY_RUN:.*--prerelease' <<< "$out" > /dev/null; then
  ok "stable version (dotnet-v4.11.0) omits --prerelease"
else
  bad "stable version unexpectedly carries --prerelease, or no command was emitted"
  echo "$out"
fi

# --- prerelease override adds --prerelease ----------------------------------
out_pre=$(run dotnet 4.12.0-rc.1)
if grep -qE 'DRY_RUN:.*--prerelease' <<< "$out_pre"; then
  ok "prerelease override (4.12.0-rc.1) adds --prerelease"
else
  bad "prerelease override did not add --prerelease"
  echo "$out_pre"
fi

# --- reusing an existing tag is refused: non-zero exit, no gh command ------
out_dup=$(run dotnet 4.10.0)
dup_exit=$?
if [[ $dup_exit -ne 0 ]] && ! grep -q 'DRY_RUN: gh release create' <<< "$out_dup"; then
  ok "reusing an existing tag (dotnet-v4.10.0) is refused with no gh command emitted"
else
  bad "reusing an existing tag was NOT refused (exit=$dup_exit)"
  echo "$out_dup"
fi

exit $fail
