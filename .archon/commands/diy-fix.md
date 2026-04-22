---
description: "Small post-workflow tweak to the active video composition — auto-detects target, runs in isolated context, returns diff summary"
argument-hint: <change description> [--for <AnimationName>]
---

<objective>
Apply a small late-stage fix to the currently active video composition WITHOUT loading the full workflow context (research, plan, scripts, sync JSONs, all scene code) into the main conversation.

This dispatches the `diy-fixer-agent` via the Task tool so the heavy reading/editing happens in an isolated subagent. The main context only receives a short diff summary.

**Use when**: typos, SFX volume tweaks, color/theme adjustments, timing nudges, small scene edits — anything that doesn't require running a full phase.
**Don't use for**: new scenes, full script rewrites, new Shorts version. For those, run the relevant phase command (`/diy-yt-creation:phase2-script`, `/diy-yt-creation:phase6-shorts`, etc.).
</objective>

<process>

## Dispatch

Call the Task tool ONCE with:

```
subagent_type: "diy-fixer-agent"
prompt: "$ARGUMENTS"
```

The agent will:
1. Resolve the active composition (marker file `.claude/diy-active.txt`, git mtime fallback, or `--for <Name>` override)
2. Classify the change (text-edit, scene-visual, sfx-volume, color-theme, timing-resync, script-edit-cascade, rebuild-scene, etc.)
3. Read only the minimum files needed
4. Apply the edit via `Edit`
5. Run the narrowest validation that applies (`pnpm lint`, `validate-sync.ts`)
6. For cascade classes, chain into `diy-phase-runner` for audio/sync regen
7. Return a <200-word structured summary

## When the Agent Returns

- **Status: done** → present the agent's summary verbatim to the user, then stop. Do NOT re-read any files to "verify" — trust the agent's validation.
- **Status: needs-clarification** → the agent couldn't classify the change. Pass the clarifying question to the user.
- **Status: out-of-scope** → the fix is too big. Suggest the appropriate phase command.
- **Status: failed** → report the error. If it's a "could not identify active composition" error, ask the user to pass `--for <Name>` and re-dispatch.

## What This Command Does NOT Do

- Does NOT render. If the summary says "user should re-render", wait for explicit user confirmation, then run the render command yourself from the main context.
- Does NOT load the brief, plan, script, or sync JSONs into main context — the agent handles all of that internally.
- Does NOT trigger QA, fact-check, or retention strategy phases. If the user wants those, they run the phase commands directly.

</process>

<examples>

```
/diy-yt-creation:fix lower the SFX volume in scene 3
```

```
/diy-yt-creation:fix fix the typo "Anthrpic" in the hook
```

```
/diy-yt-creation:fix --for DockerSandboxes change accent color to #8b5cf6
```

```
/diy-yt-creation:fix regen audio for scene 2 after I edited the script
```

</examples>
