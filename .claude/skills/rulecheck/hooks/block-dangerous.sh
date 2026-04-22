#!/bin/bash
# PreToolUse hook: block dangerous commands from rulecheck agents.
# Prevents destructive rm operations and accidental renders.
#
# Input: JSON on stdin with tool_input.command
# Output: exit 0 to allow, exit 2 + stderr message to block.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# No command found — not a Bash tool call, allow
if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block rm -rf with absolute paths (allow within node_modules or .claude/)
if echo "$COMMAND" | grep -qE 'rm\s+-rf?\s+/'; then
  if ! echo "$COMMAND" | grep -qE '(node_modules|\.claude/)'; then
    echo "Blocked: rm -rf with absolute paths is not allowed from this agent." >&2
    exit 2
  fi
fi

# Block remotion render (full video renders are expensive)
if echo "$COMMAND" | grep -qE 'remotion\s+render'; then
  echo "Blocked: full video renders are not allowed from rulecheck. Use remotion still for QA." >&2
  exit 2
fi

exit 0
