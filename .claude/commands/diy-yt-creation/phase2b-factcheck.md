---
description: "Phase 2b: Fact-check all claims, stats, quotes, and sources before audio generation"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 2b of the DIY YouTube Video Creation Workflow.

**Goal**: Verify every factual claim in the script before spending money on TTS audio generation. Zero tolerance for unverified statistics, misattributed quotes, or dead source links.
**Input**:
  - `src/$ARGUMENTS/scripts/full-script.md` (raw script with stats/claims)
  - `src/$ARGUMENTS/scripts/scene-NN-<name>.txt` (TTS-optimized scene files)
  - `src/$ARGUMENTS/research/content-brief.md` (proof points table with source URLs)
**Output**: `src/$ARGUMENTS/scripts/fact-check-report.md`
**Gate condition**: All CRITICAL claims must be VERIFIED or CORRECTED. Zero FAILED verdicts in Tier 1.
</objective>

<autonomous-mode>
## When Called from full-auto-v2

Run all steps automatically. Use WebSearch for every claim. If `PERPLEXITY_API_KEY` is set in `.env`, also run Perplexity deep-verify via `python scripts/perplexity-verify.py`. If all Tier 1 claims pass, proceed to Phase 3 immediately. If any Tier 1 claim fails, STOP orchestration and report the specific failures with corrections.
</autonomous-mode>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 2a (TTS Script) is `done`.
  - If not: STOP and report "Phase 2a (TTS Script) has not been completed. Run `/diy-yt-creation:phase2a-script $ARGUMENTS` first."
- **Re-run check**: If Phase 2b is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

---

## Step 1: Extract All Factual Claims

Read these files:
1. `src/$ARGUMENTS/scripts/full-script.md` — the narrative script
2. `src/$ARGUMENTS/research/content-brief.md` — proof points table with sources
3. All `src/$ARGUMENTS/scripts/scene-NN-*.txt` files — final TTS scripts

### Claim Extraction Rules

Scan every sentence for factual claims. A "claim" is any statement that could be independently verified as true or false. Extract into a structured list:

**Tier 1 — CRITICAL (must verify, blocks gate)**:
- Statistics with numbers ("24 million secrets", "40% higher", "$4.67M average cost")
- Direct quotes attributed to named people ("Jensen Huang said...", "Andrej Karpathy wrote...")
- Financial/legal data (costs, fines, breach amounts)
- Security/safety claims that could cause harm if wrong
- Year-specific data ("in 2024", "as of 2025")

**Tier 2 — IMPORTANT (must verify, advisory warning if unverified)**:
- Product feature claims ("supports X", "works with Y", "includes Z")
- Version numbers and release dates ("v2.3 released in March")
- Comparative claims ("faster than X", "more secure than Y")
- Market position claims ("most popular", "industry standard")
- GitHub stars, downloads, contributor counts (change rapidly)

**Tier 3 — CONTEXTUAL (best-effort verification, advisory only)**:
- General technical descriptions ("React uses a virtual DOM")
- Well-known historical facts ("Docker launched in 2013")
- Industry consensus ("microservices improve scalability")

### Output Format for Extraction

For each claim, record:
```
| # | Claim Text | Tier | Scene | Source URL (from brief) | Verification Method |
```

Report total: "Found X claims: Y Tier 1, Z Tier 2, W Tier 3"

---

## Step 2: Verify Claims

### Method A: WebSearch (ALWAYS — for every Tier 1 and Tier 2 claim)

For each Tier 1 and Tier 2 claim:

1. **Search with year filter**: Always include the current year or the year claimed in the search query. Never trust training data alone for statistics.
   - Example: `"GitHub secret scanning 2024 statistics"`, `"IBM data breach cost 2025 report"`
2. **Cross-reference minimum 2 sources**: A single search result is not sufficient for Tier 1 claims. Find at least 2 independent sources that agree.
3. **Prefer primary sources**: Official reports, press releases, earnings transcripts, and documentation over blog posts or news articles.
4. **Check recency**: If the claim says "2024" but the best source is from 2023, flag as STALE.
5. **Verify exact numbers**: "nearly 24 million" vs "23.8 million" — the script can round, but the underlying number must be correct.

### Method B: Perplexity API (OPTIONAL — when `PERPLEXITY_API_KEY` is set)

Check `.env` for `PERPLEXITY_API_KEY`. If present:

```bash
python scripts/perplexity-verify.py $ARGUMENTS
```

This script:
1. Reads the extracted claims from the script
2. Sends each Tier 1 claim to Perplexity's `sonar` model with citation-required prompts
3. Returns structured verdicts with source citations
4. Writes results to `src/$ARGUMENTS/scripts/perplexity-results.json`

If `PERPLEXITY_API_KEY` is NOT set, skip this step and rely on WebSearch alone. Log: "Perplexity API not configured — using WebSearch only. Set PERPLEXITY_API_KEY in .env for deeper verification."

### Method C: URL Liveness Check (for all source URLs in content-brief)

For every URL listed in the content-brief's Proof Points table:
1. Use WebFetch to check if the URL returns a 200 response
2. Verify the page content actually supports the claimed statistic
3. Flag dead links (404, 403, timeout) as BROKEN

### Method D: Technical Accuracy Spot-Check

For claims about specific tools, libraries, or APIs:
1. Check official documentation via WebSearch
2. Verify feature claims match current version (not deprecated/removed)
3. Check that code examples in the script are syntactically valid

---

## Step 3: Render Verdicts

For each claim, assign one of these verdicts:

| Verdict | Meaning | Action Required |
|---------|---------|-----------------|
| **VERIFIED** | Claim confirmed by 2+ sources | None |
| **CORRECTED** | Claim was slightly wrong, fix applied | Script update needed |
| **STALE** | Claim uses outdated data, newer data available | Script update needed |
| **UNVERIFIED** | Could not confirm or deny | Tier 1: BLOCKS gate / Tier 2: Warning |
| **FAILED** | Claim is demonstrably false | Script update REQUIRED |
| **BROKEN_SOURCE** | Source URL is dead or doesn't support claim | Replace URL needed |

### Correction Protocol

When a claim is CORRECTED or STALE:
1. Record the original claim text
2. Record the corrected value with source
3. Provide the exact replacement text for the script
4. Note which scene file(s) need updating

**IMPORTANT**: Do NOT auto-edit the script files. Present corrections to the user (or in full-auto mode, apply corrections and log them). The user must approve before re-generating audio.

---

## Step 4: URL & Resource Audit

This step verifies resources planned for the YouTube description.

Read `src/$ARGUMENTS/research/content-brief.md` and extract all URLs from:
- Proof Points source URLs
- Any "Resources" or "Links" sections
- Referenced documentation, blog posts, reports

For each URL:
1. **Liveness**: Does it resolve? (WebFetch)
2. **Relevance**: Does the page content match what it's cited for?
3. **Recency**: Is there a newer version of this resource? (e.g., "2024 report" when "2025 report" exists)
4. **Primary vs Secondary**: Is this the original source or a secondary blog post? Flag secondary sources and suggest the primary.

---

## Step 5: Generate Fact-Check Report

</process>

<output>

### Report Structure

Save to: `src/$ARGUMENTS/scripts/fact-check-report.md`

```markdown
# Fact-Check Report: $ARGUMENTS
Generated: [DATE]
Verification methods: WebSearch [+ Perplexity API if used]

## Summary

| Metric | Count |
|--------|-------|
| Total claims extracted | N |
| Tier 1 (Critical) | N |
| Tier 2 (Important) | N |
| Tier 3 (Contextual) | N |
| VERIFIED | N |
| CORRECTED | N |
| STALE | N |
| UNVERIFIED | N |
| FAILED | N |
| Source URLs checked | N |
| Broken sources | N |

**Overall Verdict**: PASS / FAIL

## Gate Result

- Tier 1 FAILED count: N (must be 0 to pass)
- Tier 1 UNVERIFIED count: N (must be 0 to pass)
- Broken critical sources: N

**PASS condition**: Zero Tier 1 FAILED + Zero Tier 1 UNVERIFIED + Zero broken Tier 1 sources

## Tier 1 Claims (Critical)

| # | Scene | Claim | Verdict | Sources | Notes |
|---|-------|-------|---------|---------|-------|
| 1 | Scene 02 | "23.8M secrets leaked on GitHub in 2024" | VERIFIED | [GitGuardian 2025 Report](url) | Exact match |
| 2 | Scene 03 | "70% of leaked secrets still valid" | CORRECTED | [GitGuardian](url) | Was "70%", actual is "69%" — rounded OK |

## Tier 2 Claims (Important)

| # | Scene | Claim | Verdict | Sources | Notes |
|---|-------|-------|---------|---------|-------|

## Tier 3 Claims (Contextual)

| # | Scene | Claim | Verdict | Sources | Notes |
|---|-------|-------|---------|---------|-------|

## Source URL Audit

| # | URL | Status | Supports Claim? | Notes |
|---|-----|--------|-----------------|-------|
| 1 | https://... | LIVE | Yes | Primary source |
| 2 | https://... | BROKEN (404) | N/A | Need replacement |

## Corrections Required

If any claims need updating, list each with:

### Correction 1: [Scene NN]
- **Original**: "24 million secrets were leaked in 2024"
- **Corrected**: "23.8 million secrets were leaked in 2024"
- **Source**: [GitGuardian State of Secrets Sprawl 2025](url)
- **File to update**: `src/$ARGUMENTS/scripts/scene-02-problem.txt`
- **Impact**: Minor rounding — acceptable as "nearly 24 million" in spoken script

## Stale Data Warnings

List any claims using data older than 12 months where newer data exists.
```

### Gate Decision

**On PASS** (zero Tier 1 FAILED, zero Tier 1 UNVERIFIED):

All critical claims verified. Script is factually sound.

If corrections were applied: list the specific changes made.
If Tier 2 warnings exist: list as advisories but do not block.

Next step: Run `/diy-yt-creation:phase3-audio $ARGUMENTS`

**On FAIL** (any Tier 1 FAILED or UNVERIFIED):

STOP. Do NOT proceed to Phase 3.

Numbered list of blocking issues:
1. Which claim failed, in which scene
2. What the correct information is (with source)
3. Exact replacement text for the script

After corrections, re-run: `/diy-yt-creation:phase2b-factcheck $ARGUMENTS`

### Auto-Correction Mode (full-auto only)

When running in full-auto mode and corrections are minor (rounding, date updates, URL swaps):
1. Apply corrections directly to the scene `.txt` files
2. Log every change in the report under "Auto-Applied Corrections"
3. Do NOT re-run TTS optimization — the corrections are small enough to not affect pronunciation
4. Proceed to Phase 3

When corrections are major (wrong statistic, misattributed quote, false claim):
1. STOP orchestration
2. Report the failure with exact issues
3. User must review and approve before continuing

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md`:
- If all gates **PASS**: set the `2b - Fact Check` row to `done (N/N claims verified)` with today's date.
- If any gate **FAILS**: set the `2b - Fact Check` row to `blocked (N failed claims)` with today's date.

If the file doesn't exist, create it with all phases as `pending` first.
</output>
