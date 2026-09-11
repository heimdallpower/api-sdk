#!/usr/bin/env bash
# Table-driven tests for the pure bump-suggestion logic in prepare-release.sh
# (suggest_bump, has_breaking_footer, resolve_bump). The functions are
# extracted rather than sourced — sourcing would run the script's own
# arg-parsing and git/gh calls.
#
# Run: bash .github/scripts/prepare-release.test.sh
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
src="$here/prepare-release.sh"
fail=0

extract() { sed -n "/^$1() {/,/^}/p" "$src"; }
for fn in suggest_bump has_breaking_footer resolve_bump; do
  body=$(extract "$fn")
  if [[ -z "$body" ]]; then
    echo "FAIL setup: could not extract $fn() from $src"
    exit 1
  fi
  eval "$body"
done

# check_bump <want> <subject-line>...
# One or more subject lines -> suggest_bump's verdict.
check_bump() {
  local want=$1; shift
  local subjects got
  subjects=$(printf '%s\n' "$@")
  got=$(printf '%s\n' "$subjects" | suggest_bump)
  if [[ "$got" == "$want" ]]; then
    echo "ok   suggest_bump($*) -> $got"
  else
    echo "FAIL suggest_bump($*) -> $got (want $want)"
    fail=1
  fi
}

# check_resolve <want> <subject> <body>
# subject+body -> resolve_bump's verdict (type from subject, breaking footer
# from body only as a line-anchored footer).
check_resolve() {
  local want=$1 subject=$2 body=$3 got
  got=$(resolve_bump "$subject" "$body")
  if [[ "$got" == "$want" ]]; then
    echo "ok   resolve_bump($subject) -> $got"
  else
    echo "FAIL resolve_bump($subject) -> $got (want $want)"
    fail=1
  fi
}

# --- suggest_bump: type from subject line(s) ---
check_bump none ""
check_bump none "chore(pip): Bump ruff from 0.16.3 to 0.16.4 (#155)"
check_bump none "chore: POWER-5025 Update to .NET 10 (#146)"   # documented v4.0.0 under-call, expected wrong answer
check_bump patch "fix(python): handle missing auth token gracefully"
check_bump minor "feat: add new endpoint for circuit ratings"
check_bump minor "feat(dotnet): POWER-4075 add proxy configuration for API client"
check_bump major "feat!: drop net9.0"
check_bump major "feat(dotnet)!: drop net9.0"
check_bump major "refactor!: rename DTOs"
check_bump minor "fix: a" "feat: b" "fix: c"      # highest wins
check_bump patch "chore: x" "fix: y" "chore: z"

# --- resolve_bump: a dependabot body must not poison the type ---
dependabot_body=$'Bumps [PyJWT](https://github.com/jpadilla/pyjwt) from 2.8.0 to 2.10.1.\n- feat: add minimum key length validation for HMAC and RSA\n- fix: reject tokens with invalid algorithm\n- fix: another upstream fix line'
check_resolve none "chore(deps): bump the pip-dependencies group with 1 update" "$dependabot_body"

# --- resolve_bump: BREAKING CHANGE footer still detected when line-anchored ---
breaking_body=$'Some prose describing the change.\n\nBREAKING CHANGE: removes the legacy endpoint'
check_resolve major "refactor: drop legacy endpoint" "$breaking_body"

# --- resolve_bump: mid-line mention of BREAKING CHANGE is NOT a footer ---
prose_body=$'This commit message mentions BREAKING CHANGE in prose, not as a footer.'
check_resolve none "chore: tidy up docs" "$prose_body"

exit $fail
