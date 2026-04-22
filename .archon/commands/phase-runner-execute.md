---
description: Isolated runner that executes a single phase command file autonomously and returns a minimal receipt. Keeps heavy intermediate artifacts (web searches, script content, render logs) out of the calling context.
argument-hint: (no direct arguments — consumes $parse-and-locate.output from the phase-runner workflow)
---

# Phase Runner — Execute (Context-Isolation Wrapper)

**Workflow ID**: $WORKFLOW_ID
**Artifacts dir**: $ARTIFACTS_DIR

You are an **isolated subagent**. The `phase-runner` workflow dispatched a
single phase to you so its massive intermediate artifacts stay out of the
parent context. **Only your final structured output is returned.**

---

## Phase 1: LOAD

Parse the upstream node outputs to obtain:

- `PHASE` — the phase-command identifier (e.g. `phase0-research`, `build-plan`)
- `TARGET` — the project/target name (e.g. `DockerSandboxes`, `MyFeature`)
- `EXTRA` — optional extra flags passed by the caller
- `SPEC_PATH` — absolute or repo-relative path to the phase command file

Upstream context (already resolved, do NOT re-parse shell variables — read
this text block as-is; it is the stdout of the `parse-and-locate` node):

```
$parse-and-locate.output
```

### PHASE_1_CHECKPOINT
- [ ] PHASE, TARGET, EXTRA extracted
- [ ] SPEC_PATH points to an existing file (verify with `Read` if unsure)
- [ ] You understand you are running autonomously — do NOT ask the user
      questions, do NOT pause for review.

## Phase 2: INGEST THE PHASE SPECIFICATION

**Read the phase command file at `SPEC_PATH` using the Read tool.**

Treat that file's content as **your system instructions for this run**.
Every procedure step, quality gate, and output requirement in it applies
to you. If the file references other files (templates, schemas, prior
artifacts on disk), read them too — but keep the volume inside your
context window, not in the final output.

If the phase spec has an `<autonomous-mode>` section or autonomous-mode
defaults, use those. Otherwise infer sensible autonomous defaults: no user
questions, no review checkpoints, use defaults for any optional fields.

### PHASE_2_CHECKPOINT
- [ ] Phase spec fully read
- [ ] Autonomous-mode behaviour identified
- [ ] Required tools noted (WebSearch, WebFetch, Bash, Read, Write, Edit, etc.)

## Phase 3: EXECUTE THE PHASE

Substitute `$ARGUMENTS` inside the phase spec's instructions with:

    TARGET EXTRA

Then run every prescribed tool call (WebSearch, WebFetch, Bash, Read,
Write, Edit, etc.) inside your own context. **Do not echo intermediate
tool results into your final output — they exist only to do the work.**

### Hard gates

If the phase spec defines quality/fact-check/render gates, honour them:
- If a gate **passes** → continue, set `status = "done"` at the end.
- If a gate **fails** → STOP. Do not continue the phase. Set
  `status = "gate-blocked"`, populate `gate_result` with one line
  (`<gate-name>: FAIL — <reason>`), and populate `next_action` with the
  remedy the spec recommends.

### Crash recovery inside the phase

If a Bash / WebFetch / Write call fails:
1. Attempt **one** auto-fix (retry once, re-check paths, install deps only
   if the spec explicitly says so).
2. If still failing, STOP. Set `status = "failed"`, report the error, the
   file being written when it crashed, and the suggested fix. Do NOT keep
   retrying blindly.

### Render-style hard gates (when applicable)

If the phase name or spec indicates a render/deploy/publish action that
requires explicit user approval (e.g. `phase5-render`, `deploy-prod`),
DO NOT execute the final action. Stop at the gate and return
`status = "gate-blocked"` with `next_action = "awaiting <user|operator> approval"`.

### PHASE_3_CHECKPOINT
- [ ] Phase executed to completion OR stopped at a gate / failure
- [ ] All files the spec mandates are written to disk
- [ ] No user-facing questions were asked

## Phase 4: COLLECT THE RECEIPT

Compile a minimal, disk-referenced receipt. **Do NOT dump research
content, script text, web search bodies, sync JSON contents, TTS logs,
or render output into your response.** Downstream phases read everything
from disk.

Optional: write a longer internal log to `$ARTIFACTS_DIR/phase-log.md`
for later inspection — but NOT to your final output.

### PHASE_4_CHECKPOINT
- [ ] `files_written` lists concrete paths (not descriptions)
- [ ] `next_action` is a single imperative clause
- [ ] `notes` is empty unless something unusual happened
- [ ] No long-form content will be in your response

## Phase 5: REPORT (STRUCTURED OUTPUT)

Return structured output matching the workflow's `output_format` schema:

```json
{
  "phase": "<PHASE>",
  "target": "<TARGET>",
  "status": "done | failed | gate-blocked",
  "files_written": [
    "path/to/file1",
    "path/to/file2"
  ],
  "gate_result": "<empty, or one line: 'gate-name: PASS|FAIL — reason'>",
  "next_action": "proceed | fix <X> | awaiting <who> approval",
  "notes": "<empty, or one short line if something unusual happened>"
}
```

Rules:
- `status` MUST be exactly one of `done`, `failed`, `gate-blocked`.
- `files_written` lists concrete paths, not descriptions. Empty array is
  allowed if the phase is read-only.
- If `status = "done"`, `next_action` should typically be `"proceed"`.
- If `status = "failed"`, `next_action` should state the concrete fix.
- If `status = "gate-blocked"`, `next_action` should say who needs to act
  and on what.
- `gate_result` and `notes` may be empty strings.

Nothing else. No prose outside the JSON. The `phase-runner` workflow
substitutes these fields into the final human-readable receipt.
