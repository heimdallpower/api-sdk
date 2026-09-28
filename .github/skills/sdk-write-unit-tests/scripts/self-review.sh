#!/usr/bin/env bash
# Self-review checks for SDK unit tests. Run from the repo root:
#   bash .github/skills/sdk-write-unit-tests/scripts/self-review.sh [base-ref]   # default: origin/main
# Prints findings per check; every finding needs a fix or a stated reason.
# shellcheck disable=SC2013 # paths and keys contain no spaces; word splitting is intended
set -uo pipefail

base=${1:-origin/main}
here="$(cd "$(dirname "$0")" && pwd)"
dn_tests=dotnet/tests/unit
py_tests=python/tests/unit

section() { printf '\n== %s\n' "$1"; }

section "1. Test files driving the fake transport without asserting the request"
# Paths have no spaces; plain word splitting keeps this bash 3.2 (macOS /bin/bash) compatible.
for f in $(grep -rl --include='*.cs' 'RecordingHttpMessageHandler' "$dn_tests" | grep -v '/Fakes/'); do
  grep -q 'QueryString.Of\|AbsolutePath\|RequestUri' "$f" || echo "  $f"
done
for f in $(grep -l 'RecordingTransport' "$py_tests"/test_*.py 2>/dev/null); do
  grep -q 'last_params\|url.path\|last_request' "$f" || echo "  $f"
done

section "2. Tests changed since $base whose only assertions are weak (non-null / non-empty / status)"
changed=$(git diff --name-only "$base" -- "$dn_tests" "$py_tests" | while read -r f; do [ -f "$f" ] && echo "$f"; done)
# shellcheck disable=SC2086 # one path per word
[ -n "$changed" ] && python3 "$here/find-weak-tests.py" $changed

section "3. New public properties / model fields since $base not referenced in unit tests"
for p in $(git diff "$base" -U0 -- dotnet/HeimdallPower.Api.Client | grep -oE '^\+ +public [^(=]+ [A-Z][A-Za-z]+ \{ get' | awk '{print $(NF-2)}' | sort -u); do
  grep -rqw --include='*.cs' "$p" "$dn_tests" || echo "  .NET:   $p"
done
for f in $(git diff "$base" -U0 -- 'python/heimdall_api_client/*_api_client/models/*.py' | grep -oE '^\+    [a-z_]+: ' | awk '{print $2}' | tr -d : | sort -u); do
  [ "$f" = additional_properties ] && continue   # generator boilerplate on every model
  grep -rqw "$f" "$py_tests" || echo "  Python: $f"
done

section "4. New client methods/parameters since $base without a Python signature guard"
for m in $(git diff "$base" -U0 -- python/heimdall_api_client/client.py | grep -oE '^\+ +def (get_[a-z_]+)' | awk '{print $NF}' | sort -u); do
  grep -rq "\"$m\"" "$py_tests" || echo "  Python: $m not in any test list (e.g. test_endpoint_wrappers_resolve.py)"
done
