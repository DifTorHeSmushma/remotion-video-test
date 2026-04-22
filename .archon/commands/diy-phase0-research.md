---
description: "Phase 0: Research a topic deeply — gather facts, features, stats, and messaging for video content"
argument-hint: <topic, product URL, or concept to research OR a brief.md file based on the template .claude\commands\diy-yt-creation\brief-template.md>
---

<objective>
Execute Phase 0 of the DIY YouTube Video Creation Workflow.
Perform deep research on "$ARGUMENTS" to produce a comprehensive, **video-content-aware** content brief that will feed into video planning and script writing.

This workflow uses **parallel research agents** to gather information 3-4x faster than sequential research, then synthesizes findings with quality gates.

**Goal**: Understand the topic thoroughly — features, benefits, differentiators, audience pain points, compelling angles, AND how each piece of information translates to a compelling video scene.
**Output**: `src/<AnimationName>/research/content-brief.md`
</objective>

<autonomous-mode>
## When Called from full-auto-v2

If this phase is invoked as part of the full-auto-v2 orchestration, parameters will be passed in context.
**DO NOT ask questions** — use the provided values or infer sensible defaults:

- **Topic type**: Infer from URL/description (product if it has features, concept if it's technology)
- **Target viewer**: Default to "developers and technical audience" unless specified
- **Key angle**: Determine from research — find the most compelling differentiator
- **Duration**: Use to determine research depth (15s = LIGHT, 60-180s = STANDARD, 3min+ = DEEP)

Proceed autonomously through all waves.
</autonomous-mode>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: None — Phase 0 can always run.
- **Re-run check**: If Phase 0 is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

---

## WAVE 0: Parse & Pre-Fetch (Lead — synchronous)

### Step 0A: Identify Input Type

Determine what "$ARGUMENTS" refers to and classify it:

| Input Pattern | Classification | Pre-Fetch Action |
|---------------|---------------|-----------------|
| URL (http/https) | Infer from page content | Fetch URL content for all agents |
| Product/tool name | `PRODUCT_TOOL` | Search for official site |
| Abstract concept | `CONCEPT` | No pre-fetch, agents search |
| Article/video response | `ARTICLE_RESPONSE` | Fetch article URL |
| "X vs Y" or comparison | `COMPARISON` | Search both subjects |
| Brief template (has "**Topic**:") | `STRUCTURED_BRIEF` | Parse fields, fetch links |

Store as `TOPIC_TYPE` for agent prompts.

### Step 0B: Determine Research Depth

Based on target duration (from context or PARAMS):

| Duration | Depth Level | Agent A Scope | Agent B Competitors | Agent C Hook Angles |
|----------|------------|--------------|--------------------|--------------------|
| < 60s | `LIGHT` | 3 key sources | 2 alternatives | 2 angles |
| 60-180s | `STANDARD` | 5 key sources | 3 alternatives | 3 angles |
| 3-8min | `DEEP` | 8+ sources | 5 alternatives | 3+ angles |

Default to `STANDARD` if duration is unknown.

### Step 0C: Pre-Fetch Primary URL (if applicable)

If a URL was provided, fetch the page content now. This content will be included in ALL agent prompts so they share the same primary source without redundant fetches.

### Step 0D: Interactive Scoping (standalone execution only)

**Interactive mode** (standalone execution) — Ask the user (one question at a time):
1. **What is this?**: Product, open-source tool, concept, or service?
2. **Target viewer**: Who should care about this? (developers, managers, marketers, general tech audience)
3. **Key angle**: What's the ONE thing viewers should remember? (speed, security, simplicity, cost savings)

**Autonomous mode** (from full-auto-v2) — Use context or defaults, do not ask.

---

## WAVE 1: Parallel Research (4 agents — concurrent)

Spawn ALL FOUR agents simultaneously using the Agent tool. Each agent gets a self-contained prompt with the topic, classification, research depth, and any pre-fetched content.

**IMPORTANT**: Use `model: "sonnet"` and `subagent_type: "general-purpose"` for all 4 agents. Spawn all 4 in a SINGLE message to maximize parallelism.

---

### Agent A: Core Topic Researcher

**Focus**: Deep understanding of WHAT the topic IS — features, mechanism, docs, proof points.

**Agent prompt template** (adapt based on TOPIC_TYPE):

```
You are a research analyst preparing material for a YouTube explainer video.

TOPIC: {topic description}
TOPIC TYPE: {TOPIC_TYPE}
RESEARCH DEPTH: {LIGHT|STANDARD|DEEP}
{PRE-FETCHED CONTENT if available}

Your job: Research the CORE TOPIC deeply. Understand what it is, how it works, and why it matters.

Research these areas (adapt based on topic type):

FOR PRODUCT_TOOL:
- Official documentation / landing page
- GitHub README (if open source) — stars, contributors, release cadence
- Feature list / changelog / recent updates
- Pricing / tiers / free vs paid
- Integration ecosystem
- Security model / compliance
- Technical architecture (how it works under the hood)

FOR CONCEPT:
- How it works (technical mechanism)
- Why it matters (business/developer value)
- Current state of adoption
- Key players / implementations
- Common misconceptions
- Historical context (when did this emerge?)

FOR ARTICLE_RESPONSE:
- Deep analysis of the source article
- Author background and credibility
- Key claims and their evidence
- Counter-arguments in the discourse

FOR ALL TOPICS:
- Pain points this solves (3-5 relatable scenarios framed as "You've been there...")
- Quantifiable claims with sources (benchmarks, adoption stats, cost savings)
- Technical terms that might need TTS pronunciation notes

OUTPUT FORMAT (use these exact headers):

## Value Proposition
<One sentence: "X helps Y achieve Z by doing W">

## Target Audience
<Primary, secondary, what they know, what they care about>

## Pain Points
1. <Pain point with relatable scenario> [VISUAL POTENTIAL: HIGH/MEDIUM/LOW]
2. ...
(minimum 3, target 5)

## Features & Benefits
| Feature | Benefit (user-facing) | Differentiator? | Metric | Demo Possible? |
|---------|----------------------|-----------------|--------|---------------|
| ... | ... | Yes/No | ... | Yes/No |

## Proof Points
| Stat/Claim | Value | Comparison Baseline | Source URL | Visual Format |
|-----------|-------|-------------------|-----------|--------------|
| ... | ... | ... | ... | bar chart / counter / comparison |
(minimum 5 proof points with source URLs)

## Technical Terms (TTS Pronunciation)
| Term | Pronunciation Note |
|------|-------------------|
| ... | ... |

## Raw Research Notes
<Links, quotes, data points gathered — include everything even if not used above>
```

---

### Agent B: Competitive & Market Analyst

**Focus**: Position the topic against alternatives and the broader market.

**Agent prompt template**:

```
You are a competitive intelligence analyst preparing material for a YouTube explainer video.

TOPIC: {topic description}
TOPIC TYPE: {TOPIC_TYPE}
RESEARCH DEPTH: {LIGHT|STANDARD|DEEP}
{PRE-FETCHED CONTENT if available}

Your job: Map the competitive landscape and market context. Help the video creator position this topic against alternatives and explain WHY NOW.

Research these areas:
- Direct competitors / alternatives ({2-5 based on depth})
- Key differentiators (what THIS does that others don't)
- Notable adopters / case studies (companies, people — these become "cult-hop" references)
- Market trends and timing signal ("why NOW?" — what changed recently?)
- Industry size / growth stats
- SEO keywords people search for related to this topic (for YouTube title/description optimization)

OUTPUT FORMAT (use these exact headers):

## Competitive Landscape
| Alternative | Key Difference | Where Topic Wins | Where Alternative Wins |
|------------|---------------|-----------------|---------------------|
| ... | ... | ... | ... |

## Notable Adopters
| Company/Person | How They Use It | Why It Matters for Video |
|---------------|----------------|------------------------|
| ... | ... | cult-hop reference / social proof / etc. |

## Market Context
- Market size: ...
- Growth trajectory: ...
- Key trend driving adoption: ...

## Timing Signal (Why NOW?)
<2-3 sentences on what changed recently that makes this topic timely>

## SEO Keywords
| Keyword / Phrase | Search Intent | Monthly Volume Estimate |
|-----------------|--------------|----------------------|
| ... | ... | high/medium/low |
(minimum 5 keywords)

## Raw Research Notes
<Links, quotes, data points>
```

---

### Agent C: Hook Architecture Researcher

**Focus**: Find raw materials for maximum-retention hooks.

**Agent prompt template**:

```
You are a YouTube hook specialist and audience researcher preparing material for an explainer video.

TOPIC: {topic description}
TOPIC TYPE: {TOPIC_TYPE}
RESEARCH DEPTH: {LIGHT|STANDARD|DEEP}
{PRE-FETCHED CONTENT if available}

Your job: Find the raw materials that will make this video IMPOSSIBLE TO SCROLL PAST. Research hook elements, contrarian angles, and audience psychology.

The video uses the Kallaway Formula:
1. Context Lean-In — mind-blowing fact or shared pain point (first 4 seconds)
2. Scroll-Stop Interjection — "But/However/Yet" as a stun gun
3. Contrarian Snapback — "Uno Reverse" that snaps viewers onto unexpected path

Research these areas:

CULT-HOPPING OPPORTUNITIES (minimum 5):
- Established brands, celebrities, or cultural references that can anchor the topic
- Well-known companies/people that use this or something similar
- Familiar concepts that serve as analogies (cross-domain borrowing is powerful)
- "Known layers" that can wrap the unknown idea
- For each: WHERE in the video it should appear (hook, mid-video, CTA)

CONTRARIAN ANGLES (minimum 3):
- What's counterintuitive about this topic?
- What common belief can be challenged with evidence?
- What seems obvious but is actually wrong?
- For each: what EVIDENCE supports the contrarian claim? (no unsupported hot takes)

MIND-BLOWING STATS (minimum 5 candidates):
- Surprising metrics or benchmarks WITH source URLs
- Counterintuitive data points
- Comparison statistics that shock (e.g., "X is bigger than Y" where Y is unexpected)
- Rate each: SHOCK FACTOR 1-10 (how likely to cause a scroll-stop)

COMPETITOR VIDEO ANALYSIS:
- Search YouTube for existing videos on this topic
- What hooks do they use? What angles do they take?
- What do they MISS that we can cover?
- What do YouTube comments say? (viewer objections to preempt)

COMMON GROUND BY AUDIENCE:
- Technical audience: What shared professional pain point resonates?
- General audience: What everyday metaphor explains the concept?
- Decision makers: What business outcome matters most?

OUTPUT FORMAT (use these exact headers):

## Cult-Hopping References
| Brand/Person/Concept | Why It Works | Where to Use (Hook/Mid/CTA) |
|---------------------|-------------|---------------------------|
| ... | ... | ... |

## Contrarian Angles (Uno Reverse)
1. **<Angle title>**: <Description>
   - Evidence: <source URL or data point>
2. ...
(minimum 3)

## Mind-Blowing Stats
| Stat | Value | Shock Factor (1-10) | Source URL |
|------|-------|-------------------|-----------|
| ... | ... | ... | ... |
(minimum 5 candidates)

## Common Ground by Audience
- **Technical**: <shared pain point>
- **General**: <everyday metaphor>
- **Decision Makers**: <business outcome>

## Competitor Video Analysis
| Video/Channel | Hook Used | Angle | What They Miss |
|--------------|-----------|-------|---------------|
| ... | ... | ... | ... |

## Viewer Objections to Preempt
1. <Objection viewers will have> — <How to address it in the script>
2. ...

## Primary Open Loop Suggestion
- **Setup** (Scene 01-02): <The question or tension to raise early>
- **Resolution** (Scene 06-08): <Where and how to resolve it>

## Preview Hook Teasers (3 lines for Scene 00)
1. <Bold stat or claim — the scroll-stop opener>
2. <Teaser referencing a mid-video reveal>
3. <Promise statement — "In this video...">

## Raw Research Notes
<Links, quotes, data points>
```

---

### Agent D: Video Production Researcher

**Focus**: Research specifically for VIDEO content — how to SHOW, not just tell. This agent is what makes the workflow **video-content-aware**.

**Agent prompt template**:

```
You are a video production researcher and visual storyteller preparing material for a Remotion (React-based) explainer video.

TOPIC: {topic description}
TOPIC TYPE: {TOPIC_TYPE}
RESEARCH DEPTH: {LIGHT|STANDARD|DEEP}
{PRE-FETCHED CONTENT if available}

Your job: For every key concept in this topic, answer: "How do we SHOW this, not just tell it?" Research visual metaphors, demo opportunities, and scene-ready data that will make this video visually compelling.

Research these areas:

VISUAL METAPHORS:
- What real-world or cross-domain metaphors explain abstract concepts?
  (e.g., Swiss Cheese Model for layered safety, J-curve for adoption dip, Roulette Wheel for token prediction)
- What spatial metaphors work? (pipelines, funnels, layers, networks, timelines)
- For each metaphor: what concept does it explain, and how would it animate?

DEMO OPPORTUNITIES:
- Can we SHOW the tool/concept working? (screenshots, code snippets, terminal output)
- Are there before/after transformations that work as split-screen scenes?
- Are there live demos, GIFs, or videos from the creators we could reference?
- What would a "wow moment" demo look like?

SCREENSHOT OPPORTUNITIES:
- Which web pages should we capture as real screenshots? (product homepages, GitHub repos, docs pages, dashboards, blog posts)
- For each: exact URL, which section/area to capture, dark or light mode preference
- Note any pages likely to have auth walls, anti-bot protections, or heavy dynamic loading
- Prioritize pages where the REAL UI is more compelling than a recreation

SCENE-READY DATA POINTS:
- Statistics formatted for animation (number + unit + comparison baseline)
- Data suitable for bar charts, counters, or comparison tables
- Percentages, growth rates, time savings — anything that can be a visual number reveal

ARCHITECTURE / DIAGRAM OPPORTUNITIES:
- Does the topic have a system architecture that can be progressively revealed?
- Are there flowcharts, pipelines, or decision trees?
- What components connect to what? (for box-and-arrow diagrams)

EXISTING VISUAL TREATMENTS:
- How have conference talks visualized this concept?
- What infographics exist?
- What do other YouTube videos show on screen for this topic?

OUTPUT FORMAT (use these exact headers):

## Visual Metaphor Inventory
| Concept | Metaphor | How It Animates | Source/Inspiration |
|---------|----------|----------------|-------------------|
| ... | ... | ... | ... |
(minimum 3 metaphors)

## Demo Opportunities
| What to Demo | Format (screenshot/code/terminal/diagram) | URL (if screenshot) | Dark/Light | Wow Factor (1-10) | Notes |
|-------------|------------------------------------------|---------------------|------------|-------------------|-------|
| ... | ... | https://... or N/A | dark/light/N/A | ... | ... |

## Scene-Ready Data Points
| Data Point | Animated Value | Comparison Baseline | Visual Format |
|-----------|---------------|-------------------|--------------|
| ... | ... | ... | bar chart / counter / side-by-side / etc. |

## Before/After Transformations
| Before State | After State | Visual Treatment |
|-------------|------------|-----------------|
| ... | ... | split-screen / morph / timeline / etc. |

## Architecture Diagram Opportunities
| System/Flow | Components | Progressive Reveal Order | Complexity |
|------------|-----------|------------------------|-----------|
| ... | ... | ... | simple/medium/complex |

## Visual Concepts (Detailed Descriptions)
1. **<Visual name>**: <Detailed description of the visual, how it would look on screen, colors, motion, timing>
2. ...
(these feed directly into Phase 1 scene planning)

## Suggested Scene Structure
| # | Scene Name | Duration Estimate | Key Visual | Key Stat/Quote |
|---|-----------|------------------|-----------|---------------|
| 00 | Preview Hook | 5-10s | ... | ... |
| 01 | Hook | 15-25s | ... | ... |
| ... | ... | ... | ... | ... |

## Hero Visual Recommendation
<The ONE visual that should be the thumbnail / most memorable moment of the video. Describe it in detail.>

## Raw Research Notes
<Links, visual references, screenshots found>
```

---

## WAVE 2: Synthesis + Quality Gates (Lead — synchronous)

After ALL four agents return their results, synthesize findings into the final content brief.

### Step 2A: Merge & Deduplicate

Review all 4 agent outputs and:
1. **Deduplicate** — remove redundant findings that appear in multiple agents' output
2. **Cross-reference stats** — if Agent C found a stat and Agent A found the same stat with a different value, investigate which source is more authoritative
3. **Resolve conflicts** — if agents disagree on positioning or audience, use Agent A's primary research as the authority

### Step 2B: Tag Visual Potential

For EVERY proof point, feature, and pain point, assign a visual potential tag:
- **HIGH** — Agent D identified a specific visual treatment (metaphor, diagram, demo)
- **MEDIUM** — Concept is visual but no specific treatment identified yet
- **LOW** — Abstract concept, best as text-on-screen with narration

### Step 2C: Build Messaging Hierarchy

Construct the Must/Should/Could/Omit hierarchy using TWO criteria:
1. **Message importance** — how essential is this to understanding the topic?
2. **Visual showability** — can we SHOW this compellingly? (from Agent D's assessment)

Items that are both important AND visually showable go to "Must Include."
Items that are important but hard to visualize may still be "Must Include" but flagged as needing creative treatment.

### Step 2D: Construct Narrative Arc

Build the Kallaway Formula narrative arc using:
- Agent C's hook materials (contrarian angles, mind-blowing stats, cult-hop references)
- Agent A's feature hierarchy
- Agent D's scene structure suggestion
- Agent B's timing signal for "why NOW?"

### Step 2E: Generate Suggested Video Titles

Based on research findings, generate 3-5 video title options:
- At least one stat-led title
- At least one contrarian/provocative title
- At least one "how to" / solution-oriented title
- All under 60 characters for YouTube display

### Step 2F: Run Quality Gates

| Gate | Check | Threshold | Action on Fail |
|------|-------|-----------|---------------|
| QG-0A | Proof points found | >= 5 with source URLs | **FAIL** — list specific gaps in "Gaps / Needs User Input" |
| QG-0B | Contrarian angles found | >= 3 with evidence | **FAIL** — report gap, suggest the lead research more |
| QG-0C | Visual metaphor suggested | >= 1 | **WARN** — suggest using a generic spatial metaphor |
| QG-0D | Demo opportunity identified | >= 1 | **WARN** — flag to user that the video may lack demo moments |
| QG-0E | SEO keywords found | >= 3 | **WARN** — suggest manual keyword research |
| QG-0F | All proof points sourced | URLs present for each | **FAIL** — mark unsourced claims in proof points table |
| QG-0G | Cult-hop references found | >= 3 | **WARN** — suggest expanding references |

**FAIL** = report specific gap in "Gaps / Needs User Input" section. In autonomous mode, proceed but flag prominently.
**WARN** = advisory note in the brief, does not block.

### Step 2G: Write Content Brief

Assemble the enriched content brief and write to disk.

</process>

<output>
**Save to**: `src/<AnimationName>/research/content-brief.md`

The content brief uses this enriched template (ALL sections are mandatory unless marked OPTIONAL):

```markdown
# Content Brief: <Topic>

## Video Metadata
- **AnimationName**: `<PascalCase>`
- **Duration**: <target duration>
- **Tone**: <tone>
- **Target Audience**: <primary and secondary>
- **Key Angle**: <the ONE thing viewers should remember>
- **Topic Type**: <PRODUCT_TOOL | CONCEPT | ARTICLE_RESPONSE | COMPARISON>
- **Research Depth**: <LIGHT | STANDARD | DEEP>

---

## Core Value Proposition
<One sentence: "X helps Y achieve Z by doing W">

---

## Target Audience
**Primary**: <who, what they know, what they care about>
**Secondary**: <who else might watch>
**What they know**: <baseline knowledge level>
**What they care about**: <motivations>

---

## Pain Points
1. **<Pain point title>**: <relatable scenario> [VISUAL: HIGH/MEDIUM/LOW]
2. ...
(minimum 3, target 5)

---

## Key Features & Benefits
| Feature | Benefit (user-facing) | Differentiator? | Metric | Visual Potential | Demo? |
|---------|----------------------|-----------------|--------|-----------------|-------|
| ... | ... | Yes/No | ... | HIGH/MED/LOW | Yes/No |

---

## Proof Points (Scene-Ready)
| Stat/Claim | Formatted Value | Comparison Baseline | Source URL | Visual Format | Shock Factor |
|-----------|----------------|-------------------|-----------|--------------|-------------|
| ... | "21% more tasks" | vs pre-AI baseline | https://... | bar chart | 7/10 |
(minimum 5, all must have source URLs — unsourced claims marked with ⚠️)

---

## Visual Concepts
1. **<Visual name>**: <Detailed description — what it looks like, how it animates, colors, timing>
2. ...
(from Agent D — these feed directly into Phase 1 scene planning)

---

## Visual Metaphor Inventory
| Concept | Metaphor | How It Animates | Source/Inspiration |
|---------|----------|----------------|-------------------|
| ... | ... | ... | ... |

---

## Demo Opportunity Inventory
| What to Demo | Format | URL (if screenshot) | Dark/Light | Wow Factor | Notes |
|-------------|--------|---------------------|------------|-----------|-------|
| ... | screenshot/code/terminal/diagram | https://... or N/A | dark/light/N/A | 1-10 | ... |

---

## Before/After Transformations (OPTIONAL)
| Before State | After State | Visual Treatment |
|-------------|------------|-----------------|
| ... | ... | split-screen / morph / timeline |

---

## Architecture Diagram Opportunities (OPTIONAL)
| System/Flow | Components | Reveal Order | Complexity |
|------------|-----------|-------------|-----------|
| ... | ... | ... | simple/medium/complex |

---

## Competitive Landscape
| Alternative | Key Difference | Where Topic Wins | Where Alternative Wins |
|------------|---------------|-----------------|---------------------|
| ... | ... | ... | ... |

---

## Notable Adopters
| Company/Person | How They Use It | Why It Matters for Video |
|---------------|----------------|------------------------|
| ... | ... | cult-hop / social proof / credibility |

---

## Market Context & Timing Signal
- **Market size**: ...
- **Growth**: ...
- **Why NOW**: <what changed recently>

---

## Messaging Hierarchy
### Must Include [Visual Treatment]
- <item> [<visual approach from Agent D>]
- ...

### Should Include
- ...

### Could Include
- ...

### Omit
- ...

---

## Hook Architecture

### Cult-Hopping References
| Brand/Person/Concept | Why It Works | Where to Use (Hook/Mid/CTA) |
|---------------------|-------------|---------------------------|
| ... | ... | ... |
(minimum 3)

### Common Ground by Audience
- **Technical**: <shared pain point>
- **General**: <everyday metaphor>
- **Decision Makers**: <business outcome>

### Contrarian Angles (Uno Reverse)
1. **<Angle>**: <description>
   - Evidence: <source URL or data>
2. ...
(minimum 3)

### Mind-Blowing Stats
| Stat | Value | Shock Factor (1-10) | Source URL |
|------|-------|-------------------|-----------|
| ... | ... | ... | ... |
(minimum 5 candidates)

### Preview Hook Teasers (for Scene 00)
1. <Bold stat or claim — the scroll-stop opener>
2. <Teaser referencing a mid-video reveal>
3. <Promise statement — "In this video...">

### Primary Open Loop Suggestion
- **Setup** (early): <question or tension to raise>
- **Resolution** (late): <where and how to resolve it>

---

## Suggested Narrative Arc (Kallaway Formula)
1. **Context Lean-In**: <mind-blowing fact or pain point>
2. **Scroll-Stop**: <"But..." interjection>
3. **Contrarian Snapback**: <unexpected path>
4. **Solution**: <introduce the topic/product — benefit-first>
5. **Features (Benefit-Led)**: <which 3-5 features deserve scenes>
6. **Trust**: <proof point that closes the credibility gap>
7. **CTA**: <what the viewer should do next>

---

## Suggested Scene Structure
| # | Scene Name | Duration Est. | Key Visual | Key Stat/Quote |
|---|-----------|--------------|-----------|---------------|
| 00 | Preview Hook | 5-10s | ... | ... |
| 01 | Hook | 15-25s | ... | ... |
| ... | ... | ... | ... | ... |
(from Agent D, refined in synthesis)

---

## Suggested Video Title Options
1. **"<title>"** — <rationale>
2. ...
(3-5 options, all under 60 characters)

---

## SEO Keywords
| Keyword / Phrase | Search Intent | Volume Estimate |
|-----------------|--------------|----------------|
| ... | ... | high/medium/low |

---

## Technical Terms (TTS Pronunciation)
| Term | Pronunciation Note |
|------|-------------------|
| ... | Write as single word / needs spacing / phonetic guide |

---

## Viewer Objections to Preempt
1. **<Objection>**: <How to address in script>
2. ...

---

## Competitor Video Analysis (OPTIONAL)
| Video/Channel | Hook Used | What They Miss |
|--------------|-----------|---------------|
| ... | ... | ... |

---

## Quality Gate Results
| Gate | Check | Result | Notes |
|------|-------|--------|-------|
| QG-0A | Proof points >= 5 | PASS/FAIL | ... |
| QG-0B | Contrarian angles >= 3 | PASS/FAIL | ... |
| QG-0C | Visual metaphor >= 1 | PASS/WARN | ... |
| QG-0D | Demo opportunity >= 1 | PASS/WARN | ... |
| QG-0E | SEO keywords >= 3 | PASS/WARN | ... |
| QG-0F | All stats sourced | PASS/FAIL | ... |
| QG-0G | Cult-hop refs >= 3 | PASS/WARN | ... |

---

## Gaps / Needs User Input
- <Specific gap or decision needed>
- ...
(Quality gate failures are listed here automatically)

---

## Sources
| Source | URL | Used For |
|--------|-----|---------|
| ... | ... | ... |
(all URLs from all agents, deduplicated, with "Used For" column)
```

**Report to user**:
1. Summary of what was found (3-5 bullet points)
2. Recommended video angle
3. Quality gate results (pass/fail/warn counts)
4. Suggested scene count based on content density
5. Any gaps in research that need user input
6. Next step: Run `/diy-yt-creation/phase1-plan <AnimationName>` with this brief as input

### Update Phase Status

Update (or create) `src/<AnimationName>/phase-status.md`. If it does not exist, create it with this template:

    # Phase Status: <AnimationName>

    | Phase | Status | Completed |
    |-------|--------|-----------|
    | 0 - Research | pending | |
    | 1 - Plan | pending | |
    | 2 - Script | pending | |
    | 2.5 - Critique | pending | |
    | 2a - TTS Script | pending | |
    | 3 - Audio | pending | |
    | 4 - Sync | pending | |
    | 4b - Visual QA | pending | |
    | 5 - Render | pending | |
    | 6 - Shorts | pending | |
    | 6 - Upload | pending | |

Then set the `0 - Research` row to `done` with today's date.
</output>
