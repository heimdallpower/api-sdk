#!/usr/bin/env bash
# Checks the local prerequisites for building and testing both SDKs:
#
#   ./scripts/check-prerequisites.sh
#
# Installs nothing and writes no files: missing tools are reported with install
# hints. Also reports whether the integration-test credentials are present in
# HEIMDALL_CLIENT_ID / HEIMDALL_CLIENT_SECRET, without printing their values.
# Exit code 1 when a required tool is missing.
set -u

missing=0

ok()   { printf '  ok       %s\n' "$1"; }
fail() { printf '  MISSING  %s\n           hint: %s\n' "$1" "$2"; missing=$((missing + 1)); }
warn() { printf '  warning  %s\n           hint: %s\n' "$1" "$2"; }

# version_ge <have> <want>: true when dotted version <have> >= <want>
version_ge() {
  [ "$(printf '%s\n%s\n' "$2" "$1" | sort -t. -k1,1n -k2,2n -k3,3n | head -n1)" = "$2" ]
}

echo "Checking prerequisites"

# .NET: projects target net10.0; CI uses dotnet-version 10.0.x
if command -v dotnet >/dev/null 2>&1 && dotnet --list-sdks 2>/dev/null | grep -q '^10\.'; then
  ok ".NET SDK 10 ($(dotnet --list-sdks | grep '^10\.' | tail -n1 | cut -d' ' -f1))"
else
  fail ".NET SDK 10.x" "https://dotnet.microsoft.com/download/dotnet/10.0"
fi

# Python: pyproject requires-python >=3.11
py=""
for c in python3 python; do
  if command -v "$c" >/dev/null 2>&1; then py=$c; break; fi
done
if [ -n "$py" ] && "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then
  ok "Python >= 3.11 ($("$py" -c 'import platform; print(platform.python_version())'))"
else
  fail "Python >= 3.11" "https://www.python.org/downloads/"
fi

# Poetry: pyproject uses the PEP 621 [project] table, supported from Poetry 2.0
if command -v poetry >/dev/null 2>&1; then
  pv=$(poetry --version 2>/dev/null | grep -Eo '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -n1)
  if [ -n "$pv" ] && version_ge "$pv" "2.0"; then
    ok "Poetry >= 2.0 ($pv)"
  else
    fail "Poetry >= 2.0 (found: ${pv:-unknown})" "poetry self update  (or: pipx upgrade poetry)"
  fi
else
  fail "Poetry >= 2.0" "https://python-poetry.org/docs/#installation  (or: pipx install poetry)"
fi

# PowerShell 7: only needed to regenerate the Python clients
if command -v pwsh >/dev/null 2>&1; then
  ok "PowerShell 7 (pwsh)"
else
  warn "PowerShell 7 (pwsh) — only needed for python/scripts/generate-module-client.ps1" "https://learn.microsoft.com/powershell/scripting/install/installing-powershell"
fi

echo "Checking integration-test credentials"
cred_hint="set these to credentials for a Heimdall API client; contact Heimdall Power to obtain API access"
# Presence only; values are never printed.
if [ -n "${HEIMDALL_CLIENT_ID:-}" ]; then ok "HEIMDALL_CLIENT_ID is set (hidden)"
else warn "HEIMDALL_CLIENT_ID is not set — only needed for integration tests" "$cred_hint"; fi
if [ -n "${HEIMDALL_CLIENT_SECRET:-}" ]; then ok "HEIMDALL_CLIENT_SECRET is set (hidden)"
else warn "HEIMDALL_CLIENT_SECRET is not set — only needed for integration tests" "$cred_hint"; fi

if [ "$missing" -gt 0 ]; then
  echo "$missing required tool(s) missing — see hints above."
  exit 1
fi
