#!/usr/bin/env bash
# Decide whether a release tag belongs to this SDK.
#
# Usage: tag-guard.sh <dotnet|python> <tag>
#
# Writes to $GITHUB_OUTPUT (stdout if unset):
#   publish=true  version=<X.Y.Z[-pre]>   tag is this SDK's           -> exit 0
#   publish=false                          tag is the other SDK's      -> exit 0 (skip)
#   (nothing)                              anything else, incl. vX.Y.Z -> exit 1 (fail)
#   (nothing)                              unknown <sdk> argument      -> exit 2 (usage error)
#
# Three states on purpose: the other SDK's tag must not show a red X here, but
# a malformed tag must fail loudly rather than have both workflows skip green.
set -euo pipefail

sdk=${1:-}
tag=${2:-}
out=${GITHUB_OUTPUT:-/dev/stdout}

# SemVer 2 prerelease identifier: numeric (no leading zeroes) or alphanumeric
# (at least one non-digit; hyphens allowed, so `alpha-1` is valid).
ident='(0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*)'

case "$sdk" in
  dotnet) other=python; pre="(-${ident}(\.${ident})*)?" ;;      # NuGet: any SemVer 2 prerelease
  python) other=dotnet; pre='(-(alpha|beta|rc)\.[0-9]+)?' ;;    # PyPI: must normalise under PEP 440
  *) echo "::error::unknown sdk '$sdk' (expected dotnet or python)"; exit 2 ;;
esac

semver='[0-9]+\.[0-9]+\.[0-9]+'
mine_re="^${sdk}-v(${semver}${pre})$"
other_re="^${other}-v"

if [[ "$tag" =~ $mine_re ]]; then
  version=${BASH_REMATCH[1]}
  echo "publish=true" >> "$out"
  echo "version=$version" >> "$out"
  echo "::notice::$tag is a $sdk release tag; publishing version $version"
  exit 0
fi

if [[ "$tag" =~ $other_re ]]; then
  echo "publish=false" >> "$out"
  echo "::notice::$tag is a $other release tag; nothing to do for $sdk"
  exit 0
fi

echo "::error::Invalid release tag '$tag' for $sdk."
echo "::error::Expected ${sdk}-v<MAJOR>.<MINOR>.<PATCH>[-prerelease], e.g. ${sdk}-v4.1.0. The unprefixed vX.Y.Z format is retired — see CONTRIBUTING.md § Branching & Releases."
exit 1
