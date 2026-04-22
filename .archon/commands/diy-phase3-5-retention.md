---
description: "Phase 3.5: Analyze script/sync data and produce per-scene retention component strategy"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 3.5 of the DIY YouTube Video Creation Workflow.
Analyze the composition's script, plan, and audio sync data to produce a concrete per-scene retention strategy.

**Goal**: Map each scene to specific retention components with exact props and triggerFrames, so the Phase 4 scene builder has content-aware decisions rather than generic rules.
**Input**:
  - `.agents/plans/$ARGUMENTS.plan.md` (from Phase 1)
  - `src/$ARGUMENTS/scripts/full-script.md` (from Phase 2)
  - `src/$ARGUMENTS/scripts/sceneNN-sync.json` (from Phase 3)
  - `src/$ARGUMENTS/constants/timing.ts` (from Phase 3)
**Output**: `src/$ARGUMENTS/retention-strategy.md`
</objective>

<process>

## Phase Gate

Check prerequisites:
- [ ] `src/$ARGUMENTS/scripts/scene01-sync.json` exists (Phase 3 complete)
- [ ] `src/$ARGUMENTS/constants/timing.ts` exists (Phase 3 complete)

If not met: "Phase 3 must complete before Phase 3.5. Run `/diy-yt-creation/phase3-audio $ARGUMENTS` first."

---

## Execution

**Spawn `retention-strategy-agent` as an isolated subagent** (prevents sync JSON data from flooding main context):

Use the **Task tool**:
```
Task tool:
  subagent_type: "retention-strategy-agent"
  prompt: "$ARGUMENTS"
```

Wait for result. The agent writes `src/$ARGUMENTS/retention-strategy.md` to disk autonomously.

---

## After Agent Returns

1. Confirm `src/$ARGUMENTS/retention-strategy.md` exists
2. Read the Summary Table section from the strategy file
3. Report to user:

```
## Retention Strategy Complete: {AnimationName}

{agent summary}

### Scene Type Breakdown
{summary table from strategy file}

### Action Required by Phase 4
The phase4-scene-builder will read retention-strategy.md automatically.
No manual changes needed unless you want to override any decisions.

### Override Instructions
To change a decision: edit `src/{AnimationName}/retention-strategy.md` directly.
The file is human-readable. Phase 4 reads it as-is.

Next step: Run `/diy-yt-creation/phase4-sync {AnimationName}`
```

## Update Phase Status

Update `src/$ARGUMENTS/phase-status.md`:
- Set `3.5 - Retention` row to `done {today's date}`

</process>
