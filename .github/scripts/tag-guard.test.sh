#!/usr/bin/env bash
# Table-driven tests for tag-guard.sh. Run: bash .github/scripts/tag-guard.test.sh
set -uo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
fail=0

# expect <sdk> <tag> <want_exit> <want_publish|-> <want_version|->
expect() {
  local sdk=$1 tag=$2 want_exit=$3 want_publish=$4 want_version=$5
  local tmp got_exit got_publish got_version
  tmp=$(mktemp)
  GITHUB_OUTPUT="$tmp" bash "$here/tag-guard.sh" "$sdk" "$tag" >/dev/null 2>&1
  got_exit=$?
  got_publish=$(sed -n 's/^publish=//p' "$tmp"); got_publish=${got_publish:--}
  got_version=$(sed -n 's/^version=//p' "$tmp"); got_version=${got_version:--}
  rm -f "$tmp"
  if [[ "$got_exit" == "$want_exit" && "$got_publish" == "$want_publish" && "$got_version" == "$want_version" ]]; then
    echo "ok   $sdk $tag"
  else
    echo "FAIL $sdk $tag -> exit=$got_exit publish=$got_publish version=$got_version (want exit=$want_exit publish=$want_publish version=$want_version)"
    fail=1
  fi
}

# Own prefix -> publish, version stripped of prefix
expect dotnet dotnet-v4.1.0           0 true 4.1.0
expect python python-v4.1.0           0 true 4.1.0
expect dotnet dotnet-v4.1.0-beta.1    0 true 4.1.0-beta.1
expect dotnet dotnet-v4.1.0-preview.2 0 true 4.1.0-preview.2
expect python python-v4.1.0-rc.1      0 true 4.1.0-rc.1
expect python python-v4.1.0-beta.1    0 true 4.1.0-beta.1
expect python python-v4.1.0-alpha.3   0 true 4.1.0-alpha.3
expect dotnet dotnet-v4.1.0-alpha-1   0 true 4.1.0-alpha-1   # hyphen is legal in a SemVer identifier
expect dotnet dotnet-v4.1.0-rc.1.2    0 true 4.1.0-rc.1.2    # dot-separated identifiers

# Other SDK's prefix -> skip green, no version
expect dotnet python-v4.1.0           0 false -
expect python dotnet-v4.1.0           0 false -
expect dotnet python-v0.0.1-test      0 false -   # bad python tag is python's problem, not dotnet's

# Retired unprefixed format -> fail red on BOTH sdks
expect dotnet v4.1.0                  1 - -
expect python v4.1.0                  1 - -
expect dotnet v9.9.9-test             1 - -

# Malformed -> fail red
expect dotnet dotnet-v4.1             1 - -
expect dotnet dotnet-v4.1.0-          1 - -   # empty prerelease
expect dotnet dotnet-v4.1.0-..        1 - -   # empty identifiers
expect dotnet dotnet-v4.1.0-01        1 - -   # leading zero in a numeric identifier
expect python python-v0.0.1-test      1 - -   # not PEP 440
expect python python-v4.1.0-preview.1 1 - -   # valid PEP 440, but not accepted here
expect dotnet garbage                 1 - -

# Unknown sdk argument -> exit 2
expect ruby ruby-v1.0.0               2 - -

exit $fail
