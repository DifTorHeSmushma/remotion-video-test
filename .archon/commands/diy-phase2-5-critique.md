---
description: "Phase 2.5: LLM script critique loop -- five-pass quality gate before TTS"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 2.5 of the DIY YouTube Video Creation Workflow.

**Goal**: Catch structural problems in the script before expensive audio generation. Run a four-pass automated critique that gates progress to Phase 2a.
**Input**: `src/$ARGUMENTS/scripts/full-script.md` (from Phase 2)
**Output**: `src/$ARGUMENTS/scripts/critique-report.md`
**Gate condition**: Hook Score >= 7.0 AND Story Arc Score >= 7.0 AND Loop Opener count >= required minimum AND banned phrase count == 0

If ANY gate fails, the script is BLOCKED from proceeding to Phase 2a until the issue is fixed and Phase 2.5 is re-run.
</objective>

<autonomous-mode>
## When Called from full-auto-v2

Run all five passes automatically. If all gates pass, proceed to Phase 2a immediately. If any gate fails, STOP orchestration and report which gate(s) failed with specific actionable issues. Do not ask questions.
</autonomous-mode>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 2 (Script) is `done`.
  - If not: STOP and report "Phase 2 (Script) has not been completed. Run `/diy-yt-creation:phase2-script $ARGUMENTS` first."
- **Re-run check**: If Phase 2.5 is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

## Step 1: Read the Script

### Plan File Discovery

Locate the plan file using this priority:
1. `.agents/plans/$ARGUMENTS.plan.md` (direct match by AnimationName)
2. If not found, glob `.agents/plans/*.plan.md` and find the file whose kebab-case name
   best matches $ARGUMENTS split on PascalCase boundaries
   (e.g., `ClaudeCodeDesktop` -> look for a file containing `claude-code-desktop`)
3. If still not found, STOP and ask the user for the plan file path. Do NOT proceed without a plan.

Store the resolved path as `PLAN_FILE` for all subsequent references.

Read the following files:
- `src/$ARGUMENTS/scripts/full-script.md` — the script to critique
- `PLAN_FILE` — the video plan (for open loop references and hook variants)
- `.claude/references/story-locks.md` — reference for Loop Opener definitions

Calculate these metrics from the script:
- `total_word_count` — sum of all scene word counts
- `estimated_duration_seconds` = total_word_count / 2.5
- `estimated_duration_minutes` = estimated_duration_seconds / 60
- `mid_video_word_target` = total_word_count x 0.58

Report:
```
Script: src/$ARGUMENTS/scripts/full-script.md
Total words: N
Estimated duration: Xm Ys (N seconds)
Mid-video word target (58%): N words
```

---

## Pass 1: Hook Strength Scoring (Quality Gate 1)

Analyze the hook scenes (Scene 00 Preview + Scene 01 Hook). Score five dimensions:

### Dimension 1 — Curiosity Gap Strength (1-10)
- 9-10: Single sentence creates immediate, unambiguous curiosity gap
- 7-8: Curiosity gap present but takes 2-3 sentences to establish
- 5-6: Some curiosity but could be dismissed
- 3-4: Informational opening, no gap created
- 1-2: Generic introduction, no hook

### Dimension 2 — Stakes Clarity (1-10)
- 9-10: Specific, quantified stakes ("you will waste 6 months rebuilding")
- 7-8: Stakes are clear but general ("this will save you significant time")
- 5-6: Implied stakes, viewer must infer
- 3-4: Benefits mentioned but stakes not established
- 1-2: No stakes established

### Dimension 3 — Specificity (1-10)
- 9-10: Specific stat or number in opening line ("73% of devs...")
- 7-8: Named tools or specific examples within first 30 seconds
- 5-6: Some specificity but could be more concrete
- 3-4: Generic language throughout hook
- 1-2: Completely abstract

### Dimension 4 — Scroll-Stop Interjection (0 or 2)
Presence of But/However/Yet/Although pivot within the hook.

### Dimension 4b — Value Alignment (0 or 0.5)
Does the hook name the video's main topic/feature within the first 2 sentences?
- 0.5: Feature/concept named directly — viewer knows what they'll learn by second 4
- 0: Hook creates tension/curiosity without naming the subject — viewer must wait to learn what the video is about

### Dimension 5 — Promise Statement (0 or 1)
Explicit promise of resolution ("In the next X minutes, you will...").

### Scoring Formula

```
base = (D1 + D2 + D3) / 3
stun_bonus = D4 / 20        # 0.0 or 0.1 (reduced)
alignment_bonus = D4b       # 0.0 or 0.5
hook_score = min(10, round(base + stun_bonus + alignment_bonus + D5, 1))
```

**Quality Gate 1**: Hook Score MUST be >= 7.0 to proceed.

### Output Format

| Dimension | Score | Notes |
|-----------|-------|-------|
| Curiosity Gap | X/10 | [specific observation] |
| Stakes Clarity | X/10 | [specific observation] |
| Specificity | X/10 | [specific observation] |
| Stun Gun | X/2 | [present/absent + exact phrase if present] |
| Value Alignment | X/1 | [Hook names the video's subject within first 2 sentences? Yes/No] |
| Promise | X/1 | [present/absent] |
| **HOOK SCORE** | **X.X/10** | **PASS / FAIL (threshold: 7.0)** |

**On FAIL**: Provide 2-3 specific replacement sentences, not general advice. Point to exact lines that need rewriting.

---

## Pass 2: Retention Curve Analysis (Quality Gates 3 + 4)

### Check 1 — Loop Openers (Quality Gate 4)

Find all loop openers in the script. These are transition phrases between scenes that reset the viewer's attention hourglass:
- Curiosity bridges: "But here is what nobody talks about", "And this is where it gets interesting"
- Stakes escalation: "This is where most people go wrong", "Here is the part that changes everything"
- Re-engagement: "Now here is the real question", "But wait — there is more to this"

Required minimum = max(2, floor(estimated_duration_minutes / 1.5))

**QG-4 passes** if found >= required.

List each found loop opener:

| # | Scene | Position | Loop Opener Phrase |
|---|-------|----------|-------------------|
| 1 | Scene 02 | Opening | "But that is just the beginning." |
| 2 | Scene 04 | Transition | "Here is where it gets interesting." |

Result: X found, Y required — **PASS / FAIL**

### Check 2 — Boxer's Rhythm (Advisory)

Audit 3 random body paragraphs. Flag if any 5-sentence stretch has all sentences within +/- 3 words of each other in length (monotonous rhythm). This check is advisory — it does not block the gate.

### Check 4 — Hedging Language (Advisory)

Search for: "if you", "might", "maybe", "could be", "probably", "perhaps", "you may", "might want to".

List all occurrences with scene and line. Suggest embedded-truth replacements (e.g., "you might want to try" -> "try this").

This check is advisory — it does not block the gate, but high hedging count (5+) indicates weak writing.

---

## Pass 3: TTS Readability Check (Advisory)

These checks are advisory — they flag potential TTS issues but do not block the gate.

### Check 1 — Scene Length Compliance

For each scene, calculate:
- `target_words` = scene_duration_seconds x 2.5
- Valid range = target_words +/- 10%

| Scene | Words | Target | Range | Status |
|-------|-------|--------|-------|--------|
| Scene 01 | N | N | N-N | OK / OVER / UNDER |

### Check 2 — Sentence Length

Flag any sentence exceeding 25 words. Long sentences are harder for TTS to deliver naturally.

### Check 3 — Acronym Safety

Known-safe acronyms (do NOT flag): AI, API, UI, CLI, SDK, PDF, HTML, CSS, JS, TS, URL, HTTP, SQL, LLM, GPU, CPU, RAM, SSD, IDE, SSH, DNS, JWT, XSS, CORS, REST, CRUD, YAML, JSON, XML, CSV, TLS, SSL, AWS, GCP

Flag any other acronym not already spaced or hyphenated for TTS. Suggest spacing (e.g., "GRPC" -> "G R P C" or "gee-RPC").

### Check 4 — Symbol Check

Scan for: { } < > [ ] $ % @ # (break tags exempt). These render as silence or gibberish in TTS.

### Check 5 — 800 Character Estimate

If scene word_count x 5.5 > 800, flag as likely too long after TTS optimization expands abbreviations.

---

## Pass 4: Story Arc Completeness (Quality Gate 2)

Score four arc elements on a 1-10 scale:

### Arc Element 1 — Hook to Value Delivery Timing
First concrete payoff must arrive before:
- 4 seconds for short-form (< 60s)
- 45 seconds for medium (60s-3min)
- 90 seconds for long-form (3min+)

| Score | Criteria |
|-------|----------|
| 9-10 | On time, high-value hit |
| 7-8 | Slightly delayed but substantive |
| 5-6 | Delivers but value is vague |
| 3-4 | Value hit missing or too late |
| 1-2 | No clear value hit |

### Arc Element 2 — Benefit-Led Feature Scenes
Do scene-opening sentences mention viewer problem or gain BEFORE technical explanation?

| Score | Criteria |
|-------|----------|
| 9-10 | Every scene benefit-led |
| 7-8 | >= 75% of scenes benefit-led |
| 5-6 | Mixed |
| 3-4 | Mostly feature-led |
| 1-2 | All feature-led (information dump) |

### Arc Element 3 — CTA Strength
Must pass all three: debate-sparking question + specific video reference + under 15 words.

| Score | Criteria |
|-------|----------|
| 9-10 | All three criteria met |
| 7-8 | Two criteria met |
| 5-6 | One criterion met |
| 3-4 | Generic CTA |
| 1-2 | No CTA or pure channel plug |

### Arc Element 4 — Narrative Cohesion
Logical scene flow + primary open loop resolved + clear beginning/middle/end structure.

| Score | Criteria |
|-------|----------|
| 9-10 | Tightly structured, clear arc |
| 7-8 | Mostly coherent with minor gaps |
| 5-6 | Some structural jumps |
| 3-4 | Scenes feel disconnected |
| 1-2 | No discernible arc |

### Arc Element 5 — Experience Signal (Advisory Bonus)

Does the script contain at least 1 "scar" — a first-person friction point, failure mode, undocumented edge case, or time trap that earns trust because it could not have been generated by AI?

| Score | Criteria |
|-------|----------|
| 1 | Present: specific failure mode / time wasted / undocumented edge case |
| 0 | Absent: purely informational content with no earned insight signal |

This is advisory — it does not block QG-2, but adds 0.5 bonus points to the story arc score when present, signaling that the content has credibility beyond what AI aggregation can produce.

**Scar patterns** (any of these pass): "I wasted X hours before...", "The docs don't mention...", "This breaks silently when...", "After running this on N projects I noticed...", "Here's what nobody writes about..."

**Commodity Test**: If the entire script could be reproduced by prompting ChatGPT with the video title, flag it as a credibility risk — not a gate failure, but a note for the writer to add at least one experience signal.

### Scoring Formula

```
story_arc_score = round((Arc1 + Arc2 + Arc3 + Arc4) / 4, 1)
experience_bonus = 0.5 if Arc5 == 1 else 0
story_arc_score = min(10, story_arc_score + experience_bonus)
```

**Quality Gate 2**: Story Arc Score MUST be >= 7.0 to proceed.

### Output Format

| Element | Score | Notes |
|---------|-------|-------|
| Hook to Value Timing | X/10 | [observation] |
| Benefit-Led Scenes | X/10 | [which scenes are feature-led] |
| CTA Strength | X/10 | [debate question present?] |
| Narrative Cohesion | X/10 | [open loop resolved?] |
| Experience Signal | 0 or +0.5 | [scar found / not found — quote if found] |
| **STORY ARC SCORE** | **X.X/10** | **PASS / FAIL (threshold: 7.0)** |

**On FAIL**: Provide 2-3 specific structural rewrites pointing to exact scenes that need changes.

---

## Pass 5: AI-Phrasing Detection (Quality Gate 5)

Scan `full-script.md` for phrases from the Banned Patterns list in `.claude/research/faceless-tech-scriptwriting-playbook.md` §11.

### Critical Phrases (BLOCKING — zero tolerance)

Any exact or near-match of these phrases causes QG-5 FAIL:
- "But here's the thing" / "But here is the thing" / "But here's what" / "But here's where"
- "Most developers don't know" / "Most developers missed" / "Most developers are sleeping on" / "Most people don't realize"
- "No more [X]" (as a benefits bullet pattern)
- "[X] changes everything" / "This changes everything"
- "If this helped, subscribe" / "If this changed how you think" (generic CTA pattern)

### High Phrases (BLOCKING — zero tolerance)

- "Let me show you" / "Let me walk you through"
- "Here's the thing" (standalone)
- "Game changer" / "game-changing"
- "The future of [X]"
- "Under the hood"

### Medium Phrases (ADVISORY — max 1 per video)

- "It's not just X — it's Y"
- "Nobody talks about"
- "Where it gets interesting"
- "Think about it" / "Think about that"
- "Paradigm shift"
- "Imagine [generic scenario]"

### Scoring

```
banned_count = count of Critical + High phrases found
QG-5 PASS: banned_count == 0
QG-5 FAIL: banned_count > 0
```

### Output Format

| # | Phrase Found | Severity | Scene | Suggested Alternatives |
|---|---|---|---|---|
| 1 | "But here's the thing" | Critical | Scene 03 | "One detail changes this." / "Look at what happens when..." |

Medium phrases: list as advisories (not blocking), flag if count > 1 per video.

Result: X Critical/High found — **PASS / FAIL**

**On FAIL**: List each phrase with scene location and 2-3 alternatives from the Playbook §11. The writer must replace ALL Critical/High phrases before re-running QG-5.

</process>

<output>

## Gate Summary

Produce the final gate summary table:

| Gate | Check | Result | Score/Status |
|------|-------|--------|-------------|
| QG-1 | Hook Strength | PASS / FAIL | X.X/10 (threshold: 7.0) |
| QG-2 | Story Arc | PASS / FAIL | X.X/10 (threshold: 7.0) |
| QG-3 | Loop Opener Frequency | PASS / FAIL | X found, Y required |
| QG-4 | AI-Phrasing Detection | PASS / FAIL | X banned phrases found |

**Overall Verdict**: PASS or FAIL

### On PASS

All four quality gates cleared. The script is approved for TTS optimization.

Next step: Run `/diy-yt-creation:phase2a-script $ARGUMENTS`

### On FAIL

Numbered list of specific actionable issues per failed gate. Each issue must include:
- Which gate failed
- What specifically is wrong (quote the problematic text)
- A concrete replacement or structural fix

After revisions, re-run: `/diy-yt-creation:phase2-5-critique $ARGUMENTS`

**STOP** — do NOT proceed to Phase 2a under any circumstance until all five gates are cleared.

## Save Report

Save the full critique report to: `src/$ARGUMENTS/scripts/critique-report.md`

The report must include all four passes with their output tables, the gate summary, and the overall verdict.

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md`:
- If all gates **PASS**: set the `2.5 - Critique` row to `done (X.X/10 hook, X.X/10 arc)` with today's date.
- If any gate **FAILS**: set the `2.5 - Critique` row to `blocked (<failed gate names>)` with today's date.

If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>

### Retention Checklist (Phase 2.5 — BLOCKING)

The following issues block script approval. Each must receive a PASS before Phase 2a proceeds:

- [ ] Does every scene (except final CTA) end with an open loop or chapter hook?
- [ ] Are all chapter/scene names curiosity gaps rather than topic labels?
- [ ] Is the WPM in range (150-165 WPM per segment)?
- [ ] Are high-impact reveal words preceded by `[PAUSE]` in .txt files?
