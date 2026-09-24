#!/usr/bin/env bash
# Blocks AI agent edits to generated code and release-critical files.
# Used by Claude Code hooks (PreToolUse on Edit|Write); can also be called from other tooling.
#
# Exit codes:
#   0 — file is safe to edit
#   2 — file is protected; Claude Code blocks the edit and shows the reason to the agent

# Claude Code passes tool context as JSON on stdin — extract the file path.
FILE=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""), end="")' 2>/dev/null) || FILE=""
if [[ -z "$FILE" ]]; then exit 0; fi

# Normalize path separators (Windows backslashes → forward slashes)
FILE=$(echo "$FILE" | sed 's|\\|/|g')

if echo "$FILE" | grep -qE 'python/heimdall_api_client/[a-z_]+_api_client/'; then
  echo "BLOCK: Generated client — regenerate with python/scripts/generate-module-client.ps1 instead of editing by hand." >&2
  exit 2
fi

if echo "$FILE" | grep -qE '(\.github/workflows/[a-z-]*publish\.yml|\.github/scripts/[^/]+\.sh|python/poetry\.lock)$'; then
  echo "BLOCK: Release-critical or lock file — confirm intent with the user before editing (poetry.lock: run 'poetry lock' instead)." >&2
  exit 2
fi
