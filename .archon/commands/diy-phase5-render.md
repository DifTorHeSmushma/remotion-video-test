---
description: "Phase 5: Preview, fine-tune, and render the final video"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 5 of the DIY YouTube Video Creation Workflow.
Validate, fine-tune, and render the final video for "$ARGUMENTS".

**Goal**: Ensure the composition is error-free, sync is tight, produce the final .mp4 output, and generate YouTube description.
**Input**: Complete `src/$ARGUMENTS/` composition (from Phase 4)
**Output**: `out/$ARGUMENTS/final.mp4`, `src/$ARGUMENTS/youtube-description.md`
**Reference**: `docs/plans/2026-01-24-video-creation-workflow.md` (Phase 5)
</objective>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 4 (Sync) is `done`.
  - If not: STOP and report "Phase 4 (Sync) has not been completed. Run `/diy-yt-creation:phase4-sync $ARGUMENTS` first."
  - Phase 4b (Visual QA) is opt-in. Do NOT warn if skipped — only run QA when the user explicitly requests it.
- **Re-run check**: If Phase 5 is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

## Step 1: Pre-Render Validation

### 1a: Sync Validation (MANDATORY)

Run the automated sync cross-reference:
```bash
npx tsx scripts/validate-sync.ts $ARGUMENTS --verbose
```

If **errors** are found: fix them before proceeding. Common fixes:
- `STALE_TIMESTAMP`: Update KF values from current sync JSON
- `DURATION_TOO_SHORT`: Extend scene duration in timing.ts
- `READING_TIME`: Extend phase boundary or scene duration
- `MISSING_ASSET`: Generate the missing audio/image asset

Warnings are informational — note but don't block.

### 1b: TypeScript and Lint Checks

```bash
pnpm lint
```

Fix any type errors or lint warnings before proceeding.

## Step 2: Studio Preview

Instruct the user to preview:
```bash
pnpm dev
```

Ask the user to check:
- Does text appear when the corresponding word is spoken?
- Are transitions smooth between scenes?
- Do spring animations feel natural (not too fast/slow)?
- Is the overall pacing comfortable?

## Step 3: Visual QA (SKIPPED BY DEFAULT — USER-APPROVED ONLY)

**Do NOT run QA automatically.** Skip this step and proceed to Step 4.

Only spawn `remotion-qa-agent` if the user explicitly asks for QA ("run QA", "check frames", "do visual QA", etc.). Preview-in-Studio is the primary QA method; the automated agent is opt-in.

**If the user explicitly requests QA**: spawn via Task tool with `subagent_type: "remotion-qa-agent"` and `prompt: "$ARGUMENTS"`. The agent reads `src/$ARGUMENTS/qa-frames.json`, renders each checkpoint via `npx remotion still`, and writes the report to `out/$ARGUMENTS/qa-report.md`. Apply the pass/warning/failure gate as usual.

## Step 4: Fine-Tune Sync (if needed)

Common adjustments:
- **Text appears too late**: Subtract 2-5 frames from the trigger frame
- **Text appears too early**: Add 2-5 frames to the trigger frame
- **Animation too fast**: Increase interpolation range (e.g., `[54, 70]` → `[54, 80]`)
- **Animation too slow**: Decrease interpolation range
- **Spring too bouncy**: Increase `damping` in spring config
- **Spring too stiff**: Decrease `stiffness` or increase `mass`

After adjustments, ask user to re-preview.

## Step 5: Render

**CRITICAL: NEVER start a render automatically. Always STOP and ASK the user before rendering.** Wait for explicit confirmation (e.g., "render", "go ahead", "yes").

Once the user explicitly approves, render the final video:

```bash
npx remotion render $ARGUMENTS out/$ARGUMENTS/final.mp4
```

### Render Options

**Standard quality (recommended)**:
```bash
npx remotion render $ARGUMENTS out/$ARGUMENTS/final.mp4 --codec h264 --crf 18
```

**Maximum quality** (larger file):
```bash
npx remotion render $ARGUMENTS out/$ARGUMENTS/final.mp4 --codec h264 --crf 15
```

**Quick test** (specific frame range):
```bash
npx remotion render $ARGUMENTS out/$ARGUMENTS/test.mp4 --frames=0-150
```

**YouTube optimized** (1080p, high bitrate):
```bash
npx remotion render $ARGUMENTS out/$ARGUMENTS/final.mp4 --codec h264 --crf 18 --pixel-format yuv420p
```

## Step 6: Verify Output

After render completes:
1. Check file exists at `out/$ARGUMENTS/final.mp4`
2. Report file size
3. Report video duration (should match TOTAL_FRAMES / 30)
4. Instruct user to play the final video for review

## Step 7: Post-Render (Optional)

If the user wants additional outputs:
- **GIF preview**: `npx remotion render $ARGUMENTS out/$ARGUMENTS/preview.gif --frames=0-90`
- **Thumbnail**: `npx remotion still $ARGUMENTS out/$ARGUMENTS/thumbnail.png --frame=60`
- **Different resolution**: Add `--width` and `--height` flags

## Step 8: Generate YouTube Description

Generate a comprehensive YouTube description for the video.

### 7.1 Gather Source Content

Read these files for context:
- `src/$ARGUMENTS/research/content-brief.md` - Topic context and key points
- `src/$ARGUMENTS/scripts/full-script.md` - Full narration content
- `src/$ARGUMENTS/constants/timing.ts` - Scene timing for chapters

### 7.1b vidIQ Keyword Research (MANDATORY — do NOT skip)

Before drafting any description text, run a vidIQ MCP research pass. The vidIQ tools are available under the `mcp__claude_ai_vidiq__` namespace in this environment.

**Required calls**:
1. Extract 3-5 seed keywords from the content brief (product name, framework, core concept).
2. For each seed, call `mcp__claude_ai_vidiq__vidiq_keyword_research` and capture the top 10 related keywords (volume + competition).
3. Call `mcp__claude_ai_vidiq__vidiq_outliers` with the primary topic keyword and capture the top 5 outlier video titles — these reveal framings that are currently outperforming.
4. Call `mcp__claude_ai_vidiq__vidiq_trending_videos` if the topic is time-sensitive (new product launch, version update, trending framework).

**Build the keyword shortlist** (15-25 terms): favor high-volume + low-to-medium competition terms. Group by: primary (top 3 for first 200 chars), chapter keywords (for chapter titles), hashtags (15-25 from the list), long-tail (for body prose).

**Save the research snapshot** to `src/$ARGUMENTS/research/vidiq-keywords.md` with this structure:

```markdown
# vidIQ Keyword Research — $ARGUMENTS
Generated: <YYYY-MM-DD>

## Seed Keywords
- <seed 1>
- <seed 2>
- ...

## Top Related Keywords (from vidiq_keyword_research)
| Term | Volume | Competition | Use For |
|------|--------|-------------|---------|
| ...  | ...    | ...         | hook / chapter / hashtag |

## Outlier Title Patterns (from vidiq_outliers)
- "<outlier title 1>" — framing: <what made it work>
- ...

## Trending Context (from vidiq_trending_videos, if run)
- ...

## Final Keyword Shortlist
- Primary (first 200 chars): <3 terms>
- Chapter keywords: <8-10 terms>
- Hashtags: <15-25 terms>
- Long-tail (body): <5-10 terms>
```

This file is the input to Step 7.3 — the description writer MUST use the shortlist, not invent keywords from intuition.

### 7.2 Generate Chapter Timestamps

Convert scene timing from `timing.ts` to YouTube chapter format:

```
// Formula: start_frame / 30 fps = seconds → MM:SS
// Example: 409 frames / 30 = 13.6 seconds = 0:13
```

First chapter MUST start at `0:00` for YouTube to recognize chapters.

### 7.3 Create Description

Generate `src/$ARGUMENTS/youtube-description.md` with this structure:

**IMPORTANT**: First 200 characters MUST contain keywords (topic name, version, key terms). YouTube SEO depends on this. Lead with keywords, not questions.

```markdown
[Hook paragraph 1 - KEYWORD-RICH opener: Include topic name, version, key features in first 200 chars. Example: "Claude Code v2.1.19 update: 8 bug fixes and 4 new features for Anthropic's AI coding assistant."]

[Hook paragraph 2 - Solution introduction: How does this video help?]

[Hook paragraph 3 - Call to watch: What will they gain by watching?]

What You'll Learn
✅ [Key takeaway 1 - extracted from script]
✅ [Key takeaway 2]
✅ [Key takeaway 3]
✅ [Key takeaway 4]
✅ [Key takeaway 5]
✅ [Key takeaway 6]

Why [Topic] Matters
[1 paragraph explaining the broader significance and relevance of this topic]

Chapters
0:00 [Scene 1 title - from timing.ts scene names]
0:XX [Scene 2 title]
...
[Generate from SCENES object in timing.ts, use 0:XX format not 00:XX]

Featured Concepts
[1 paragraph summarizing the main technical concepts explored in the video]

Resources
📝 [Primary documentation or tool]: [URL if known, otherwise placeholder]
[Additional relevant resources based on topic]

🚀 Want to learn agentic coding with live daily events and workshops?
Check out Dynamous AI: https://dynamous.ai/?code=646a60
Get 10% off here 👉 https://shorturl.smartcode.diy/dynamous_ai_10_percent_discount

Affiliate Partners
⚙️ n8n Cloud Automation: https://n8n.partnerlinks.io/diysmartcode
📈 vidIQ (grow your YouTube channel): https://vidiq.com/DIYSmartCode

Support the Channel
☕ Buy me a coffee: https://buymeacoffee.com/diy_smartcode

Target Audience
[Comma-separated list: developers, tech enthusiasts, etc. based on content]

Hashtags
#[Tag1] #[Tag2] #[Tag3] #[Tag4] #[Tag5] #DIYSmartCode #TechTutorial
```

### 7.4 Content Guidelines

When generating the description, **every keyword decision must map back to the vidIQ shortlist from Step 7.1b**:
- **Hook paragraphs**: First 200 characters MUST contain the top 2-3 primary terms from the shortlist. Front-load topic name, version numbers, key terms. Extract pain points and solutions from research brief.
- **What You'll Learn**: Pull 6-8 key takeaways from the script's main points.
- **Why X Matters**: Synthesize the broader context from research brief.
- **Chapters**: Include "Chapters" headline, use `0:XX` format (not `00:XX`). Each chapter title MUST include at least one shortlist term — do NOT use generic labels ("Introduction", "Conclusion"). Mirror outlier-title framings where they fit.
- **Featured Concepts**: List technologies, tools, or techniques covered (pull from shortlist long-tail terms).
- **Resources**: Include documentation links if mentioned in research; validate URLs via WebFetch; use placeholders for unknowns.
- **Hashtags**: 15-25 tags drawn directly from the shortlist hashtag group + standard channel tags (`#DIYSmartCode`). Do NOT invent hashtags that aren't in the shortlist.

### 7.5 Save Description

Write the generated description to:
```
src/$ARGUMENTS/youtube-description.md
```

</process>

<output>
**Files created**:
- `out/$ARGUMENTS/final.mp4`
- `src/$ARGUMENTS/youtube-description.md`

**Report to user**:
1. Render status (success/failure)
2. Output file path and size
3. Video duration confirmation
4. YouTube description generated with chapters
5. If issues found during preview: specific frames/scenes to revisit
6. Workflow complete! The video is ready for upload.

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md`:
- After Visual QA (Step 3): set the `4b - Visual QA` row to `done (N warnings, M failures)` with today's date.
- After Render (Step 5): set the `5 - Render` row to `done` with today's date.

If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>
