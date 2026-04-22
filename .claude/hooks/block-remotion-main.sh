#!/bin/bash
# PreToolUse hook: blocks remotion render/still in main context.
input=$(cat)
cmd=$(echo "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null || echo "$input")
if echo "$cmd" | grep -q "# remotion-agent"; then exit 0; fi
if echo "$cmd" | grep -qE "remotion render"; then echo "BLOCKED: remotion render must run in a sub-agent."; exit 1; fi
if echo "$cmd" | grep -qE "remotion still"; then echo "BLOCKED: remotion still must run via remotion-qa-agent."; exit 1; fi
exit 0
