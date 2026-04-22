---
name: rulecheck
description: |
  Autonomous Remotion rule adherence checker. Scans a SPECIFIC composition for ALL
  rule violations using 3 parallel scanner agents (critical, visual, composition),
  then fixes violations with a single fixer agent. Edits files directly — no PR, no git.
argument-hint: "<CompositionName>"
---

# Rulecheck — Parallel Scan + Fix

Launch 3 parallel scanner agents to find violations fast, then one fixer agent to resolve them.

## Step 0: Determine Target Composition

Parse `$ARGUMENTS` for a composition name (PascalCase folder name under `src/`).

- **If provided** (e.g., `/rulecheck ClaudeCodeOverview`): Use it.
- **If NOT provided**: **ASK the user** which composition to check:
  > "Which composition should I run rulecheck on? (e.g., `ClaudeCodeOverview`, `ClaudeCodeV2176`)"

Verify the directory exists:
```
Glob: src/<CompositionName>/Composition.tsx
```
If not found, tell the user and stop.

## Step 1: Launch 3 Parallel Scanners

Launch ALL THREE scanner agents **in a single message** (parallel) using the Agent tool:

1. **`rulecheck-scanner-critical`** — Tier 1: fonts, Audio in scenes, wipe, +T drift, Math.random, banned components
2. **`rulecheck-scanner-visual`** — Tier 2: hardcoded delays, div collapse, unclamped interpolations, font sizes, missing colors, whiteSpace
3. **`rulecheck-scanner-composition`** — Tier 2b/3: SFX pairing, volume caps, phase fade-outs, mandatory components, midroll integration

For each, pass the composition name as the prompt:
```
Scan composition: <CompositionName>
```

Use `subagent_type` matching the agent name. Scanners use `model: sonnet` (set in their frontmatter) for higher detection quality.

**IMPORTANT**: Launch all 3 in ONE message so they run concurrently.

## Step 2: Aggregate Findings

Once all 3 scanners complete, combine their findings into a single prioritized report.
If ALL scanners report zero violations, tell the user and stop — no fixer needed.

Format the combined report:
```
Composition: <Name>

## Tier 1 — Critical
(findings from scanner-critical)

## Tier 2 — Visual/Sync
(findings from scanner-visual)

## Tier 2b/3 — Composition & SFX
(findings from scanner-composition)

Total: N violations across M files
```

Show this report to the user BEFORE launching the fixer.

## Step 3: Launch Fixer Agent

Launch the `rulecheck-agent` with the combined report as its prompt:

```
Fix violations in: <CompositionName>

<paste the combined report here>
```

Use `subagent_type: rulecheck-agent`.

## Step 4: Report Results

When the fixer completes, relay its summary to the user. Include:
- How many violations were fixed
- Whether lint/tsc passed
- Any violations that were skipped and why

## Rules for You (Main Agent)

- **ALWAYS require a composition name** — never scan everything
- **Do NOT scan or grep yourself** — the scanner agents handle that
- **Do NOT edit any files yourself** — the fixer agent handles that
- **Launch all 3 scanners in ONE message** — this is the whole point of the optimization
- **Show the aggregated report before fixing** — let the user see what was found
- **If fixer fails or hits limits** — report what happened, don't retry yourself
