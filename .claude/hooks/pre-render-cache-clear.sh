#!/bin/bash
# PreToolUse hook: auto-clears webpack cache before any remotion render/still command.
# This eliminates the #1 friction source: stale webpack cache causing render failures.
input=$(cat)
cmd=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null || echo "$input")

# Only trigger on remotion render/still commands
if echo "$cmd" | grep -qE "remotion (render|still)"; then
  # Clear webpack cache silently
  rm -rf node_modules/.cache 2>/dev/null
  echo '{"decision": "allow", "systemMessage": "Cleared webpack cache before render."}'
  exit 0
fi

exit 0
