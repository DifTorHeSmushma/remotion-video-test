---
name: archon-tutorial
description: Create explainer videos and tutorials about Archon (the open-source AI coding workflow engine by Cole Medin / Dynamous). Use when the user asks to plan, script, research, or build a video about Archon — "what is Archon", "explain archon workflows", "how to use archon hooks", "archon DAG video", "archon tutorial", "archon.diy video", "archon hero loop", etc. Also use when planning an Archon video series, creating hero loops in the ArchonHero visual style, or when the user says "use the archon skill".
---

# Archon Tutorial Skill

Produce accurate, high-retention explainer videos about Archon — the open-source workflow engine that makes AI coding repeatable. Always ground claims in the real source code, never in memory or assumptions.

## CRITICAL: Single Source of Truth

**All factual claims about Archon MUST come from the local Archon repo**, not from training data, past conversations, or what "sounds right."

```
C:\Users\Leex279\Documents\GitHub\dynamous\Archon\
```

Before writing a single line of script, plan, or visual copy about Archon, open the repo and validate. The three layers, in order of authority:

| Layer | Path | When to use |
|---|---|---|
| **Implementation** (highest authority) | `packages/*/src/` | "Does this CLI flag / YAML key / API actually exist?" |
| **Internal design notes** | `CLAUDE.md`, `packages/*/CLAUDE.md` | "What were the design principles? Why is it built this way?" |
| **Published docs** | `packages/docs-web/src/content/docs/**/*.md` | "What's the official name / pitch / example for this concept?" |
| **Marketing pitch** | `README.md` | "What's the top-level positioning and tagline?" |

If the README and the code disagree, **the code wins**. If the docs and the code disagree, **the code wins and flag the docs as stale** (the user may want to know).

### Required Pre-Flight Check (Every Session)

Before producing any Archon content, run this validation sequence:

1. `git -C "C:\Users\Leex279\Documents\GitHub\dynamous\Archon" log -1 --format="%h %s %ad" --date=short` — confirm you're reading the current HEAD, not a stale clone
2. Skim `README.md` (first ~100 lines) — capture the current tagline and feature list
3. List bundled workflows: grep `README.md` and `packages/workflows/src/` for the current set — Cole ships/retires workflows regularly
4. Check `CHANGELOG.md` for the most recent release — every tutorial should be accurate to the latest version

Never cite a workflow, CLI command, YAML key, config flag, or feature you haven't just verified in the repo.

## Archon Mental Model (Use This as the Narrative Spine)

The single idea every Archon video should drive home:

> **Structure is deterministic. Intelligence is not constrained. You get both.**

The tagline Cole uses verbatim in docs:

> **"Archon makes your AI coding assistant predictable by giving it a process to follow."**

Analogy scaffolding that works in almost every video:
- **Recipe + Chef** — the workflow is the recipe (you write it, it's deterministic); the AI is the chef (creative, intelligent, fills in judgment calls). Same recipe, consistent results, fresh thinking.
- **Dockerfile for AI coding** — README framing. "Like Dockerfiles for infrastructure and GitHub Actions for CI/CD, Archon does that for AI coding workflows."
- **n8n for software development** — Cole's own comparison. Good for audiences who know n8n.

## Five Pillars (From README — Use Verbatim)

These five words are the canonical feature pillars. Use them as-is in hero scenes, feature breakdowns, and CTAs:

| Pillar | One-liner |
|---|---|
| **Repeatable** | Same workflow, same sequence, every time |
| **Isolated** | Every run gets its own git worktree — parallel work, no conflicts |
| **Fire and forget** | Kick off a workflow, come back to a finished PR |
| **Composable** | Mix deterministic nodes (bash, tests, git) with AI nodes |
| **Portable** | One workflow, same behavior from CLI / Web / Slack / Telegram / GitHub / Discord / Gitea / GitLab |

The `src/ArchonHeroFeatures/Composition.tsx` composition already has these pillars visualized — reuse/extend that style for any feature-breakdown scene.

## Concept Cheat Sheet

Canonical concepts and where to dig deeper in the repo. Never explain these from memory — pull the live example from the docs source before filming.

| Concept | One-liner | Source file (in `packages/docs-web/src/content/docs/`) |
|---|---|---|
| **Commands** | Markdown prompt templates in `.archon/commands/` — atomic reusable tasks | `book/first-command.md`, `guides/authoring-commands.md` |
| **Workflows** | YAML DAGs in `.archon/workflows/` that orchestrate commands + bash + loops | `book/first-workflow.md`, `guides/authoring-workflows.md` |
| **Isolation (worktrees)** | Every run gets its own git worktree; main branch never touched | `book/isolation.md` |
| **Artifacts** | Files in `$ARTIFACTS_DIR` — how nodes pass state without context rot | `book/how-it-works.md` |
| **DAG workflows** | `depends_on`, `when:`, `output_format`, `trigger_rule`, parallel execution | `book/dag-workflows.md` |
| **Conditional branching** | `when: "$classify.output.type == 'BUG'"` — skip nodes by condition | `book/dag-workflows.md` (when expressions section) |
| **Node types** | 6 types: `command`, `prompt`, `bash`, `loop`, `approval`, `cancel` | `guides/authoring-workflows.md` |
| **Hooks** | PreToolUse / PostToolUse interception — inject guidance mid-work | `book/hooks-and-quality.md`, `guides/hooks.md` |
| **Loop nodes** | Iterate until a completion signal (Ralph pattern) | `guides/loop-nodes.md` |
| **Approval nodes** | Human-in-the-loop pause with optional AI rework on reject | `guides/approval-nodes.md` |
| **Skills** | Domain-knowledge packs preloaded per node | `guides/skills.md` |
| **MCP servers** | Per-node external tool attachment (GitHub, Postgres, etc.) | `guides/mcp-servers.md` |
| **Adapters** | Web UI / CLI / Slack / Discord / Telegram / GitHub / Gitea / GitLab (8 total) | `adapters/index.md` + per-adapter files |
| **Web UI & Workflow Builder** | Visual DAG builder, command dashboard, approval UI, SSE streaming | `adapters/web.md` |
| **Global workflows** | `~/.archon/` workflows that apply across all projects | `guides/global-workflows.md` |
| **Variables** | `$ARGUMENTS`, `$nodeId.output`, `$ARTIFACTS_DIR`, `$LOOP_USER_INPUT`, etc. | `reference/variables.md` |
| **Configuration** | Config priority: env vars > repo `.archon/config.yaml` > global `~/.archon/config.yaml` > defaults | `getting-started/configuration.md`, `reference/configuration.md` |
| **AI Assistants** | Claude Code (primary) + Codex (OpenAI) as supported runtimes; PI/Open Code/AMP planned | `getting-started/ai-assistants.md` |
| **Advanced SDK options** | Per-node `effort`, `thinking`, `maxBudgetUsd`, `sandbox`, `fallbackModel` | `guides/authoring-workflows.md` (advanced section) |
| **Tool restrictions** | `allowed_tools` / `denied_tools` per node — whitelist or blacklist AI capabilities | `guides/authoring-workflows.md` |
| **Retry & resume** | Auto-retry transient errors; failed DAGs auto-resume from last succeeded node | `book/dag-workflows.md`, `reference/cli.md` |
| **Output format** | JSON Schema enforcement per node via `output_format` | `book/dag-workflows.md` |
| **Deployment** | Local (bun), Docker Desktop, Docker + cloud VPS, cloud-init | `deployment/` (5 pages) |
| **Security** | `bypassPermissions` mode, env-leak gate, per-node tool restrictions, webhook HMAC | `reference/security.md` |
| **Database** | SQLite (default, zero config) or PostgreSQL (set `DATABASE_URL`) | `reference/database.md` |
| **REST API** | Hono-based at `/api/`, OpenAPI spec at `/api/openapi.json` | `reference/api.md` |
| **Architecture** | User -> Adapter -> Orchestrator -> Workflow Engine -> AI Session -> FS/Git | `reference/architecture.md` |

### Bundled Workflows (Always Re-verify Before Filming)

As of the most recent check (April 2026), Archon ships **19 workflows** out of the box. **Re-grep `README.md` and `packages/workflows/src/` before quoting** — Cole adds/removes workflows frequently:

- `archon-assist` — general Q&A / debugging / exploration (catch-all)
- `archon-fix-github-issue` — classify -> investigate -> implement -> validate -> PR -> review -> self-fix
- `archon-idea-to-pr` — feature idea -> plan -> implement -> validate -> PR -> 5 parallel reviews -> self-fix
- `archon-plan-to-pr` — execute an existing plan -> PR
- `archon-feature-development` — lightweight implement + PR, no full review
- `archon-issue-review-full` — comprehensive fix + full multi-agent review pipeline
- `archon-smart-pr-review` — classify PR complexity -> run targeted reviewers only
- `archon-comprehensive-pr-review` — always run all 5 parallel reviewers
- `archon-create-issue` — classify -> investigate -> file GitHub issue
- `archon-validate-pr` — thorough PR validation on both branches
- `archon-resolve-conflicts` — detect -> analyze -> resolve -> validate -> commit
- `archon-architect` — scan complexity hotspots -> plan simplifications -> make changes
- `archon-refactor-safely` — safe refactor with type-check hooks
- `archon-ralph-dag` — implement PRD story-by-story in loops until complete
- `archon-adversarial-dev` — build complete applications from scratch
- `archon-piv-loop` — Plan-Implement-Validate with human-in-loop
- `archon-interactive-prd` — guided PRD creation through conversation
- `archon-test-loop-dag` — iterative test-fix cycle
- `archon-remotion-generate` — generate/modify Remotion video compositions (meta!)

## Repo Navigation Map (Where to Find What)

When a video needs a real example, pull from these paths in `C:\Users\Leex279\Documents\GitHub\dynamous\Archon\`:

| You need... | Look here |
|---|---|
| CLI commands + flags | `packages/cli/src/cli.ts`, `packages/cli/src/commands/` |
| Real workflow YAML | `packages/workflows/src/` (bundled), plus `.archon/workflows/` in any registered project |
| Adapter entry points | `packages/adapters/src/<github\|slack\|telegram\|discord\|gitea\|gitlab\|web>/` (8 adapters) |
| Worktree / isolation logic | `packages/isolation/src/` |
| Git ops | `packages/git/src/` |
| Orchestrator / DAG engine | `packages/core/src/` |
| Server (Web UI backend) | `packages/server/src/` |
| Web UI frontend | `packages/web/src/` |
| Database schema | `migrations/` + `packages/core/src/` |
| Deployment patterns | `docker-compose.yml`, `Dockerfile`, `deploy/`, `scripts/` |
| Internal design principles | `CLAUDE.md` (root, 791 lines — read first for any deep-dive video) |
| Official user docs | `packages/docs-web/src/content/docs/**` |

**Rule**: If you're tempted to write "Archon probably..." or "I think Archon does..." — STOP and grep. Every factual claim in an Archon video must resolve to a file or commit in this repo.

## Visual Style — Match ArchonHero / ArchonHeroFeatures

All Archon videos use the established ArchonHero visual system. Do not invent a new theme. Reference files:

- `src/ArchonHero/Composition.tsx` — hub + 6 adapter orbit loop (15s, 450 frames)
- `src/ArchonHeroFeatures/Composition.tsx` — 5-pillar cycling feature loop (15s, 450 frames)

### Color Palette (Copy Exactly)

```ts
const COLORS = {
  bg: '#0B1120',           // deep space background
  bgAlt: '#0E1A2E',        // alternate deep panel
  card: '#111A2E',         // glass card base
  cardActive: '#152039',   // highlighted/active pillar card
  text: '#F1F5F9',         // primary text
  textDim: '#94A3B8',      // secondary text
  textMuted: '#64748B',    // tertiary / muted text
  accentBlue: '#3B82F6',   // primary accent
  accentCyan: '#06B6D4',   // secondary accent / flowing particles
  accentPurple: '#8B5CF6', // tertiary accent
  accentGreen: '#22C55E',  // success / composable pillar
  accentPink: '#EC4899',   // portable pillar
  accentOrange: '#F97316', // fire-and-forget pillar
  line: '#1E293B',         // connection lines, dividers
};
```

### Typography

- **Primary**: `Inter` via `@remotion/google-fonts/Inter`
- **Mono / code / YAML**: `JetBrains Mono` via `@remotion/google-fonts/JetBrainsMono`
- Min font size: 20px long-form, 28px Shorts (hard floor — see `audio-design.md`)

### Visual Layer Stack (back -> front)

Use this exact layer order for every ArchonHero-style scene:

1. Dark background (`COLORS.bg`) + subtle animated grid (1px lines at ~4% alpha)
2. Drifting gradient mesh orbs (large, blurred, low opacity) for ambient energy
3. Procedural dust particles via `random('seed')`, never `Math.random()`
4. SVG connection lines (hub -> nodes) with flowing particles along the path
5. Hexagonally-positioned adapter/feature pills — glass-morphism style
6. Central Archon hub: logo + wordmark with pulsing glow
7. Top cycling headline ("What is Archon?" + rotating taglines)
8. Bottom-right YAML recipe snippet card (JetBrains Mono)
9. Bottom-left stat chip cycle ("N workflows encoded", etc.)

### Icon System

- **Lucide React** for all UI icons: `Terminal`, `Globe`, `MessageSquare`, `Send`, `MessagesSquare`, `Repeat`, `GitBranch`, `Workflow`, `Layers`, etc.
- **Brand logos** via `BRAND_LOGOS` constant from `src/shared/constants/brandLogos.ts`
- **Never use emojis as icons** — they render black in headless Chromium (see `agent-pitfalls.md`)
- **Never use Unicode geometric icons** — user dislikes them (memory: `feedback_no_unicode_icons.md`)

### Animation Principles

- **Seamless loops**: every animation period must divide evenly into 450 frames (e.g., 30, 50, 75, 90, 150). No snap on wrap.
- **Springs**: use `SPRINGS` from composition constants, pass `durationRestThreshold: 0.001`
- **Flowing particles along SVG paths**: classic ArchonHero move — particles traveling hub -> adapter on timed offsets
- **Pulsing glow**: wrap hub/logo in radial gradient with `sin(frame / period)` opacity modulation
- **No text drift / Ken Burns** — no `CameraZoom` (memory rule)

### Glass Card Pattern

```tsx
// ArchonHero glass card baseline
<div style={{
  background: `linear-gradient(135deg, ${COLORS.card}ee, ${COLORS.bgAlt}cc)`,
  border: `1px solid ${COLORS.line}`,
  borderRadius: 16,
  padding: '24px 28px',
  backdropFilter: 'blur(12px)',
  boxShadow: `0 20px 60px rgba(0,0,0,0.5), 0 0 40px ${COLORS.accentBlue}22`,
}}>
```

### Diagram Style

Archon videos are diagram-heavy. Always use the shared diagram system:

- `HubAndSpoke` — for "Archon as central orchestrator" shots
- `FlowDiagram` — for workflow DAG visualization
- `LayeredArchitecture` — for the 6-layer stack (User -> Adapter -> Orchestrator -> Engine -> AI -> FS/Git)
- `ComparisonDiagram` — for "chaotic AI vs Archon workflow" scenes
- `InfographicFlow` (dark mode) — for multi-stage process explainers
- Load the `visual-diagrams` skill for any architecture scene — it enforces gradient fills, shadows, and proper icon sizing (see `agent-pitfalls.md` on wireframe diagrams)

## Interactive Demos — CLI + Web UI Playback

Every Archon tutorial should show Archon **doing the thing**, not just talk about it. Pick the right demo mode per scene:

| Mode | Use when... | Fidelity | Effort |
|---|---|---|---|
| **Simulated CLI** (TerminalWindow) | Most CLI demos — commands, workflow runs, DAG progress | Good | Low |
| **Real CLI capture** (asciinema -> MP4) | Proof-of-life demo where viewers must see it's real | Perfect | Medium |
| **Static Web UI** (`capture-screenshot` + chrome) | Single-screen UI explainers, pricing/doc pages | Good | Low |
| **Stepped Web UI** (multiple screenshots + fake cursor) | Multi-step flows (register project -> run workflow) | Great | Medium |
| **Recorded Web UI** (OBS / agent-browser video) | Dynamic UI with streaming output, DAG live view | Perfect | High |

### Rule 0 — Fidelity Gate

Simulated demos are NOT a license to invent. **Everything you show on screen must match what Archon actually prints/displays.** Before scripting any terminal lines or UI copy:

1. Run the real command in a sandbox and capture the actual output (`archon workflow list`, `archon workflow run archon-assist "..."`, etc.)
2. Or grep the CLI source at `packages/cli/src/` and `packages/core/src/` for the exact strings printed
3. Save the captured output to `src/Archon<Topic>/demos/<name>.txt` and feed it directly to `TerminalWindow`

If you can't run it live, copy the example block from `README.md` lines 78–89 verbatim. Do not paraphrase CLI output.

### Mode 1: Simulated CLI (Default)

Use the existing `TerminalWindow` component at `src/shared/components/TerminalWindow.tsx`. It renders a macOS-style window with scrolling code body, dim-history lines, and frame-synced reveals.

**Pattern for an Archon CLI demo scene:**

```tsx
import { TerminalWindow } from '../../shared/components/TerminalWindow';
import { wordToFrame } from '../../shared/utils/cleanSyncData';
import { AUDIO_OFFSET_REST } from '../constants/timing';

const DEMO_LINES = [
  // Lines fade in as the narrator reads them. dimFactor ages earlier lines.
  { text: '$ archon workflow list', dimFactor: 0.6 },
  { text: '  archon-assist               General Q&A, debugging', dimFactor: 0.6 },
  { text: '  archon-fix-github-issue     Classify -> plan -> PR', dimFactor: 0.6 },
  { text: '  archon-idea-to-pr           Feature idea -> PR with 5 reviews', dimFactor: 0.6 },
  { text: '', dimFactor: 0.6 },
  { text: '$ archon workflow run archon-fix-github-issue --branch fix/42 "#42"' },
  { text: '  -> Creating isolated worktree on branch fix/42...' },
  { text: '  -> Classifying issue...' },
  { text: '  -> Investigating (reading 47 files)...' },
  { text: '  -> Implementing (task 1/4)...' },
  { text: '  -> Implementing (task 2/4)...' },
  { text: '  -> Tests failing - iterating...' },
  { text: '  -> Tests passing after 2 iterations' },
  { text: '  -> Code review complete - 0 issues' },
  { text: '  -> PR ready: https://github.com/you/project/pull/47' },
];

<TerminalWindow
  filename="archon"
  lines={DEMO_LINES}
  triggerFrame={wordToFrame(2.1, AUDIO_OFFSET_REST)}
  scrollEndFrame={wordToFrame(18.5, AUDIO_OFFSET_REST)}
  colorScheme="green"
  visibleLineCount={10}
/>
```

**Timing rules:**
- `triggerFrame` = the word where the narrator says "watch this" / "run this" — use `wordToFrame()`, never hardcoded
- `scrollEndFrame` = the word where the narrator finishes the demo
- The terminal auto-scrolls between those two frames, revealing lines as the narrator speaks
- For line-by-line reveal (one at a time instead of smooth scroll), split into multiple `TerminalWindow` instances each phase-gated to a word frame

**Typing animation for the input command:**
For extra punch on the command being typed, wrap just the input line in `TypeWriter` from `remotion-bits`:
```tsx
import { TypeWriter } from 'remotion-bits';
<TypeWriter text="archon workflow run archon-idea-to-pr" cursor speed={40} />
```
TypeWriter is one of the direct-import-OK remotion-bits components (see `.claude/rules/remotion-bits.md`).

**DAG progress visualization:** For workflow runs, pair the terminal with a live DAG render using `FlowDiagram` from `src/shared/components/` — nodes light up green as they complete. Place the terminal left (50% width) and the DAG right (50% width) in a two-pane layout.

### Mode 2: Real CLI Capture (asciinema -> MP4)

For "this is actually happening" proof scenes — the end-to-end demo episode, the series finale, or any case where simulated output would erode trust.

**Workflow:**

1. Install asciinema: `pipx install asciinema` (once)
2. Record the session:
   ```bash
   asciinema rec demos/archon-idea-to-pr.cast --idle-time-limit 2 --command "archon workflow run archon-idea-to-pr 'Add dark mode toggle'"
   ```
3. Convert to MP4 with `agg` (asciinema gif generator) + ffmpeg, or use `asciinema-edit` + `termtosvg`. Target 1920x1080, 30 fps.
4. Save as `public/videos/<composition>/cli-demo-<name>.mp4`
5. Embed in scene with `<OffthreadVideo>` inside a `<Sequence>` wrapper:
   ```tsx
   <Sequence from={triggerFrame} durationInFrames={clipDuration}>
     <OffthreadVideo src={staticFile('videos/archonidea2pr/cli-demo.mp4')} />
   </Sequence>
   ```
6. Wrap in the TerminalWindow chrome (title bar + traffic-light buttons) for visual consistency with simulated scenes

**Critical**: The Sequence wrapper is mandatory for phase-gated video embeds — direct `<OffthreadVideo>` in scene files breaks (memory: `feedback_video_embed_sequence.md`).

### Mode 3: Static Web UI (Screenshot + Browser Chrome)

For Web UI explainers where you show one page at a time. Use the existing `/capture-screenshot` slash command, which wraps `agent-browser` with cookie-dismissal, font loading, and viewport config.

**Workflow:**

1. Start the Archon Web UI locally: `cd C:\Users\Leex279\Documents\GitHub\dynamous\Archon && bun run dev` (Web UI at `http://localhost:5173`)
2. Register a demo project in the UI so there's realistic data to show
3. Capture each page the video needs:
   ```bash
   /capture-screenshot http://localhost:5173 --name dashboard --composition ArchonWebUIDemo --dark
   /capture-screenshot http://localhost:5173/workflows --name workflow-list --composition ArchonWebUIDemo
   /capture-screenshot http://localhost:5173/workflows/archon-assist --name workflow-detail --composition ArchonWebUIDemo
   /capture-screenshot http://localhost:5173/chat --name chat --composition ArchonWebUIDemo
   ```
4. In the scene, render with the browser chrome pattern from `.claude/rules/screenshot-capture.md`:
   ```tsx
   <div style={{ borderRadius: 12, overflow: 'hidden', border: '2px solid rgba(255,255,255,0.1)', boxShadow: '0 20px 60px rgba(0,0,0,0.5)' }}>
     {/* Title bar */}
     <div style={{ height: 36, backgroundColor: 'rgba(30,30,40,0.95)', display: 'flex', alignItems: 'center', gap: 8, paddingLeft: 14 }}>
       <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#ff5f56' }} />
       <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#ffbd2e' }} />
       <div style={{ width: 12, height: 12, borderRadius: '50%', backgroundColor: '#27c93f' }} />
       <div style={{ marginLeft: 12, fontSize: 13, color: 'rgba(255,255,255,0.5)', fontFamily: 'JetBrains Mono, monospace' }}>
         archon.diy/dashboard
       </div>
     </div>
     {/* Screenshot */}
     <Img src={staticFile('images/archonwebuidemo/dashboard.png')} style={{ width: '100%', display: 'block' }} />
   </div>
   ```

**Dismiss selectors** — if the Web UI has modals/tooltips that break the shot, add JS eval to the capture command to remove them before the screenshot fires.

### Mode 4: Stepped Web UI Flow (Multi-screenshot + Fake Cursor)

For multi-step flows (register project -> pick workflow -> run -> view progress). Capture 4–8 screenshots, then animate a fake mouse cursor between them.

**Pattern:**

1. Capture screenshots for each step (see Mode 3)
2. In the scene, render one framed screenshot at a time, crossfading between them synced to narration
3. Overlay an SVG cursor that springs from step N's click target to step N+1's click target between transitions
4. Add a `mouse-click.mp3` SFX at each click point (volume 0.12, ~16 dB below narration; never exceed 0.25 hard cap)

```tsx
const STEPS = [
  { img: 'dashboard.png',     clickX: 320, clickY: 180, kf: wordToFrame(1.2, O) },
  { img: 'project-modal.png', clickX: 960, clickY: 540, kf: wordToFrame(4.8, O) },
  { img: 'workflow-list.png', clickX: 420, clickY: 320, kf: wordToFrame(8.1, O) },
  { img: 'run-progress.png',  clickX: 0,   clickY: 0,   kf: wordToFrame(12.6, O) },
];
```

Cursor SVG path: `public/images/shared/ui/cursor-pointer.svg` (create once, reuse across all Web UI demos).

### Mode 5: Recorded Web UI Video (Dynamic Flows)

For scenes where the UI animates on its own — live DAG node coloring, streaming chat tokens, real-time dashboard updates — static screenshots can't capture it.

**Two capture paths:**

**A. agent-browser video mode** (preferred for reproducibility):
- Check the `agent-browser:references:video-recording` skill reference for the current API
- Script the full interaction in a shell script so it's reproducible:
  ```bash
  # demos/webui-workflow-run.sh
  agent-browser set viewport 1920 1080
  agent-browser open http://localhost:5173
  agent-browser wait 1500
  agent-browser video start demos/webui-workflow-run.webm
  agent-browser click @e1   # Start workflow button
  agent-browser wait 30000  # Let the workflow stream for 30s
  agent-browser video stop
  agent-browser close
  ```
- Convert webm -> mp4: `ffmpeg -i demos/webui-workflow-run.webm -c:v libx264 -crf 18 -preset slow public/videos/<comp>/webui-demo.mp4`

**B. Manual OBS capture** (when agent-browser video is insufficient):
- Record at 1920x1080, 30 fps, in a clean browser window
- Hide OS chrome / taskbar / notifications
- Save to `public/videos/<comp>/webui-demo.mp4`

**Embed pattern** — identical to Mode 2:
```tsx
<Sequence from={triggerFrame} durationInFrames={clipDuration}>
  <OffthreadVideo src={staticFile('videos/archondemo/webui-demo.mp4')} />
</Sequence>
```

### Demo Workspace Convention

Every Archon tutorial composition should have a `demos/` subdirectory next to `research/` and `scripts/`:

```
src/Archon<Topic>/
  research/
    content-brief.md
  demos/
    capture.sh              # Reproducible shell script for all captures
    cli-workflow-list.txt   # Terminal transcript (input to TerminalWindow)
    cli-workflow-run.txt
    webui-dashboard.png     # copied to public/images/archon<topic>/ by the script
    webui-flow.mp4          # copied to public/videos/archon<topic>/ by the script
  scripts/
    scene-NN-name.txt
  ...
```

The `capture.sh` script should be idempotent — re-runnable any time Archon releases a new version to refresh demos without starting from scratch.

### Archon-Specific Demo Cheat Sheet

Canonical terminal output fragments (verify against live `archon` before use):

**Workflow list output** (`archon workflow list`) — 19 workflows as of April 2026:
```
archon-assist                       General Q&A, debugging, exploration
archon-fix-github-issue             Classify -> investigate -> implement -> review -> PR
archon-idea-to-pr                   Feature idea -> plan -> build -> 5-agent review -> PR
archon-plan-to-pr                   Execute existing plan -> PR
archon-feature-development          Implement feature from plan -> PR
archon-issue-review-full            Comprehensive fix + full review pipeline
archon-smart-pr-review              Classify complexity -> targeted review
archon-comprehensive-pr-review      5 parallel reviewers + auto-fix
archon-create-issue                 Classify -> investigate -> file GitHub issue
archon-validate-pr                  Thorough PR validation on both branches
archon-resolve-conflicts            Detect -> analyze -> resolve -> validate -> commit
archon-architect                    Architectural sweep + complexity reduction
archon-refactor-safely              Safe refactor with type-check hooks
archon-ralph-dag                    PRD story-by-story loop until complete
archon-adversarial-dev              Build complete applications from scratch
archon-piv-loop                     Plan-Implement-Validate with human-in-loop
archon-interactive-prd              Guided PRD creation through conversation
archon-test-loop-dag                Iterative test-fix cycle
archon-remotion-generate            Generate/modify Remotion video compositions
```
Re-grep `README.md` before showing — list changes between releases.

**Workflow run progress** (verbatim from `README.md`):
```
Agent: I'll run the archon-idea-to-pr workflow for this.
       -> Creating isolated worktree on branch archon/task-dark-mode...
       -> Planning...
       -> Implementing (task 1/4)...
       -> Implementing (task 2/4)...
       -> Tests failing - iterating...
       -> Tests passing after 2 iterations
       -> Code review complete - 0 issues
       -> PR ready: https://github.com/you/project/pull/47
```

**Isolation list** (`archon isolation list`) — capture live, format changes regularly.

**Web UI pages** to capture once per video series (reuse across all episodes):
- `/` — landing / chat overview
- `/dashboard` — mission control (workflow run cards, approve/reject buttons)
- `/workflows` — workflow list (all 19 bundled + custom)
- `/workflows/<name>` — workflow detail + execution view
- `/workflows/builder` — **visual DAG builder** (drag-and-drop canvas, visual/split/code views — MAJOR differentiator, deserves prominent coverage)
- `/chat` — conversation interface with SSE streaming

### Fidelity Anti-Patterns (Do Not Ship These)

- **Invented flag output**: writing `archon run --verbose --watch` output when neither flag exists in `packages/cli/src/cli.ts`
- **Outdated progress format**: using the v1-era Python Archon output ("Task 12/47") in a video about the current workflow engine — they're entirely different products
- **Fake URLs**: showing `https://archon.diy/demo` as a "live demo link" when the real docs URL is `archon.diy`
- **Hallucinated workflow names**: `archon-auto-debug` or `archon-write-tests` — these don't exist, grep first
- **Mocked Web UI copy**: writing "Click the **Run Agent** button" when the real label is "Start Workflow" — always match live UI strings

When in doubt, **capture > simulate**. A real 10-second terminal clip or screenshot beats a perfect mock that's slightly wrong, because wrong details destroy credibility faster than production polish earns it.

## Series Episode Intro Pattern (MANDATORY for all Archon series episodes)

**The Archon videos are a numbered series, not standalone virals.** Standalone hooks (pain-first, "same prompt three answers", contrarian pivots) belong to the existing **ArchonOverview** / **ArchonV3Overview** compositions which already cover that territory. Series episodes need their own opening pattern.

### Why Series Intros Are Different

A series-episode viewer has different psychology than a cold viral-video viewer:

- **Standalone viewer**: Hasn't committed. Needs pain hook in first 4 seconds to earn the click. Will bounce unless the video feels essential.
- **Series viewer**: Already committed to learning about Archon (came via series link, playlist, or channel). Doesn't need fake pain. Needs **orientation** — "where does this episode fit, what am I about to learn, why this order?"

Using a generic pain hook on a series episode wastes the first 15 seconds on a frame the viewer has already self-selected past. It also **competes with the standalone overview videos** that already use the pain frame.

### The Required Intro Structure

Every series episode MUST open with a **Series Roadmap Intro** before any episode-specific content. Three beats, ~15–20 seconds total:

**Beat 1 — Series Branding (0–3s)**
- Full-screen title card: **"THE ARCHON SERIES"** in large Inter 900, ArchonHero palette
- Subtitle: the product tagline *"Make your AI coding assistant repeatable"*
- Archon logo with soft pulse + particle field background
- SFX: `HOOK_SFX.brandReveal` on title card land
- NO pain. NO contrarian. NO "you've been doing it wrong."

**Beat 2 — The Roadmap (3–12s)**
- Show the **entire series curriculum** grouped by arc:
  - 4 arc bands stacked vertically, each in its own accent color
  - Each arc has 3–4 episode chips: `EP NN — Title`
  - Arc headers: "Foundations", "Building Blocks", "Power Features", "Real Projects"
- Episodes appear with staggered spring entrance (50f apart)
- The **current episode's chip pulses + glows** at the moment it appears (e.g., Ep 1 chip lights up bright blue with ring animation)
- All other episode chips stay at dim 60% opacity
- This is the single highest-information-density moment in the episode: the viewer sees the whole learning path in one frame
- SFX: `HOOK_SFX.featureCard` on current episode's pulse

**Beat 3 — Focus + Value Promise (12–18s)**
- Non-current episode chips fade to 15% opacity (they're still visible in the background but de-emphasized)
- Current episode chip expands/scales to center focus
- Text reveal below: **"Episode N: [Title]"** with a one-sentence value promise
  - Example for Ep 1: *"Episode 1: What Archon is, why it exists, and whether you should use it."*
  - Example for Ep 3: *"Episode 3: From zero to your first real workflow in five minutes."*
- Soft bridge transition into Scene 01 content

### What This Replaces

- ❌ **No generic pain hook** on series episodes. If the episode's content naturally requires establishing a problem (like Ep 1 "what is Archon"), do it in Scene 01 as educational context, NOT as a standalone viral hook.
- ❌ **No "BUT" smash cut pivots** in the intro. Save pivots for mid-episode retention resets, not for the opening.
- ❌ **No Kallaway Context Lean-In → Scroll-Stop Interjection → Contrarian Snapback stack** on series episodes. That structure is for standalone videos.
- ❌ **No preview hook stats cascade** (the old Scene 00 pattern). The roadmap IS the preview.

### What It Keeps

- ✅ Strong first 3 seconds — still need scroll-stop visual, just via series branding instead of pain
- ✅ 5-Layer Hook compliance for the episode-specific content that follows (Scene 01 onward can still use Counterintuitive/Stakes/Number variants)
- ✅ Open-loop creation — the roadmap IS an open loop (viewer sees 13 other episodes they haven't watched yet)
- ✅ ArchonHero visual style (palette, particles, hub imagery)

### Required Plan Output for Series Episodes

When planning a series episode, include this block in the plan file:

```yaml
series_intro:
  pattern: "SeriesRoadmap"
  series_name: "The Archon Series"
  current_episode: <N>
  total_episodes: <14 or current count>

  arc_groups:
    - arc: "Foundations"
      color: "#3B82F6"      # blue
      episodes:
        - { num: 1, title: "What is Archon?" }
        - { num: 2, title: "Install & First Run" }
        - { num: 3, title: "Core Concepts" }
    - arc: "Building Blocks"
      color: "#8B5CF6"      # purple
      episodes:
        - { num: 4, title: "Writing Commands" }
        - { num: 5, title: "Writing Workflows" }
        - { num: 6, title: "Quality Control" }
        - { num: 7, title: "Built-in Workflows" }
    - arc: "Power Features"
      color: "#06B6D4"      # cyan
      episodes:
        - { num: 8, title: "Web UI & Builder" }
        - { num: 9, title: "Adapters & Remote" }
        - { num: 10, title: "MCP, Skills & Config" }
        - { num: 11, title: "Isolation & Parallel" }
    - arc: "Real Projects"
      color: "#22C55E"      # green
      episodes:
        - { num: 12, title: "Multi-Agent PR Review" }
        - { num: 13, title: "Deploy to Production" }
        - { num: 14, title: "Build Your Own" }

  episode_promise: "<one-sentence value promise specific to this episode>"
  duration_frames: 540      # 18 seconds at 30fps (Beat 1: 90f / Beat 2: 270f / Beat 3: 180f)
```

### Reusing the Roadmap Across Episodes

The series roadmap is a **shared reusable scene component** across every episode in the series. Define once in `src/shared/components/archon-series/SeriesRoadmapIntro.tsx`, accept props for `currentEpisode` + `episodePromise`, and import it into each episode's composition. That way:

- Every episode opens with the same recognizable roadmap (brand recall)
- The currently-highlighted episode shifts per composition
- The value promise is per-episode text
- If the curriculum changes (episode added/removed), you fix it in one place

The curriculum list itself lives in `src/shared/constants/archonSeriesCurriculum.ts` — shared constant, not duplicated per episode.

### Subsequent-Episode Variant

For Episodes 2–14, add a brief "Previously" beat before the roadmap:
- 2–3 seconds showing the previous episode's hero moment with label "Previously on The Archon Series"
- Then straight into the roadmap beat + current episode focus
- Total intro becomes ~20 seconds instead of ~18

This creates the "next week on..." television structure that trains viewers to watch in order and keeps them in the playlist.

### When NOT to Use the Series Intro

- **Standalone overview videos** (like the existing `ArchonOverview`, `ArchonV3Overview`) — they use standalone hooks, that's correct and shouldn't change
- **Shorts (<60s)** — too short for a roadmap beat, use the standalone pattern
- **Hero loops** — pure visual, no narrative
- **One-off announcement videos** (version releases, breaking news) — standalone pattern

## Video Types This Skill Supports

Pick the right template for the user's request. **Check if the topic is part of the Archon Series first** — if yes, use the Series Intro pattern, not a standalone hook.

| Video type | Length | Pattern | Intro style | Good first candidate |
|---|---|---|---|---|
| **Series episode** | 5–10 min | Series roadmap intro -> episode content -> next-ep teaser | **Series Roadmap** (see above) | Any Ep 1–14 of the Archon Series |
| **Standalone overview** | 5–8 min | Pain hook -> Archon's answer -> demo -> CTA | Standalone Kallaway/ContrastPivot | Already covered by `ArchonOverview`, `ArchonV3Overview` — don't duplicate |
| **How-to tutorial** (one-off) | 6–10 min | Goal -> prerequisites -> live walkthrough -> verify -> troubleshoot | Standalone direct-signal hook | "Add Archon to an existing repo" |
| **Feature deep-dive** (one-off) | 6–8 min | Hook -> mechanism -> real example -> edge cases | Standalone counterintuitive hook | Only when not covered by series |
| **Comparison** | 6–8 min | Status quo -> pain -> Archon approach -> caveats | Standalone contrast hook | "Archon vs raw Claude Code" |
| **End-to-end demo** | 8–12 min | Real task -> run workflow -> narrate every phase | Standalone stakes hook | "Idea to PR in one Archon run" |
| **Hero loop** | 15s | Pure visual, no audio, seamless loop for archon.diy | No intro (pure visual) | Extend `ArchonHero` style |
| **Short** | 45–60s | One concept, one YAML snippet, one payoff | Standalone counterintuitive | "What `depends_on` does" |

## Production Workflow — How This Skill Plugs Into Phases

This skill runs ALONGSIDE the existing `diy-yt-creation` phase pipeline. It does not replace it. Use this flow:

1. **Pre-Phase 0 (this skill)**: Run the pre-flight validation above. Lock in the topic, confirm the concept still exists in the current Archon HEAD, note the exact file paths you'll cite.
2. **Phase 0 research** (`/phase0-research`): Use the file paths from step 1 as primary sources. Pull real YAML/CLI examples verbatim. Output: `src/Archon<Topic>/research/content-brief.md`.
3. **Phase 1 plan** (`/phase1-plan`): Pin the visual style to ArchonHero (palette, fonts, diagram components). Choose 2 transitions (primary + accent) consistent with the tech/cinematic tone.
4. **Phase 2 script** (`/phase2-script`): Script MUST NOT contain hype or AI-slop phrases (see memory: `feedback_no_hype_honest_hooks.md`, `feedback_no_ai_slop_phrases.md`). Archon is a real tool — let the capabilities speak. Use "around" for any number (memory: `feedback_around_numbers.md`).
5. **Phase 2b fact-check** (`/phase2b-factcheck`): Every Archon-specific claim in the script MUST be re-verified against the repo. This is the last gate before audio generation.
6. **Phase 3 audio** (`/phase3-audio`): Standard TTS pipeline — no special steps.
7. **Phase 4 sync** (`/phase4-sync`): When building scenes, reuse the ArchonHero palette and the HubAndSpoke/FlowDiagram/LayeredArchitecture components. Do NOT invent a new theme.
8. **Phase 5 render** (`/phase5-render`): Standard render settings.

## Content Rules (Archon-Specific)

### Do
- Cite file paths from the repo when explaining how something works ("the DAG executor lives in `packages/core/src/...`") — adds credibility
- Show real YAML from `packages/workflows/src/` — viewers trust seeing actual shipped code
- Credit **Cole Medin** as creator where natural ("built by Cole Medin and the Dynamous community")
- Mention **archon.diy** as the docs URL (verified live)
- Mention the **Dynamous community** when discussing philosophy, roadmap, or how to learn more
- Use the exact product pillars: Repeatable, Isolated, Fire and forget, Composable, Portable
- Say "**repeatable**" when talking about Archon's determinism — the user's correction: Cole prefers "repeatable" over "deterministic" (memory: `feedback_cole_product_positioning.md`)
- Frame Archon as **harness engineering** — users already have skills/commands, Archon composes them (memory: `feedback_harness_engineering_framing.md`)

### Don't
- Don't invent CLI flags, YAML keys, workflow names, or feature names — grep first
- Don't say "deterministic" when "repeatable" is more accurate
- Don't confuse current Archon (workflow engine) with **Archon v1** (Python task-management + RAG) — v1 is preserved on the `archive/v1-task-management-rag` branch but is NOT the current product
- Don't cite absolute counts ("12 workflows") without re-grepping — use "around a dozen" or verify and update
- Don't claim parity with competitors you haven't verified
- Don't use hype superlatives ("revolutionary", "mind-blowing", "nobody is talking about")
- Don't promise features that are on the roadmap unless the repo confirms they've shipped

### Framing Traps to Avoid

- **"AI replaces developers"** — wrong frame. Archon is about giving developers a harness to tame AI, not replace themselves.
- **"Just prompt the AI harder"** — the opposite of Archon's thesis. The whole point is that prompts alone are unreliable; structure is the answer.
- **"Works with any LLM out of the box"** — verify against the repo. Multi-provider status changes; don't promise portability you haven't confirmed.
- **"Magic"** — never use this word about Archon. It's explicit, inspectable YAML. Lean into the transparency.

## Authority Checklist — Run Before Every Script

Tick every box before writing a single line of narration:

- [ ] I opened `C:\Users\Leex279\Documents\GitHub\dynamous\Archon\` and confirmed HEAD is recent
- [ ] I read the relevant `packages/docs-web/src/content/docs/*.md` file for this topic
- [ ] I grep'd the implementation in `packages/*/src/` to verify feature names / flags / YAML keys
- [ ] I checked `README.md` for current pillar language and tagline
- [ ] I checked `CHANGELOG.md` (or recent commits) for anything renamed or retired
- [ ] I have at least one real code/YAML snippet to show on screen, copied verbatim from the repo
- [ ] I'm ready to cite the exact file path in the script if the viewer wants to verify

If any box is unchecked, go back — don't start the script.

## Quick Reference — Files to Open First

For a fast-start on any Archon video, open these three in parallel:

```
C:\Users\Leex279\Documents\GitHub\dynamous\Archon\README.md
C:\Users\Leex279\Documents\GitHub\dynamous\Archon\CLAUDE.md
C:\Users\Leex279\Documents\GitHub\dynamous\Archon\packages\docs-web\src\content\docs\book\what-is-archon.md
```

Then open the topic-specific doc from the Concept Cheat Sheet table above.
