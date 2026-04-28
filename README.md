# remotion-from-hn

Archon workflow that turns any URL into a short voiced Remotion video.

## What it does

Pass a mode + URL via `$ARGUMENTS`:

- `""` / `"hn"` — auto-pick today's top Hacker News story
- `"article <url>"` — explainer video from an article
- `"marketing <url>"` — pitch video for a product site

Each run adds a new composition under `src/<CompId>/` and renders an mp4 into `./videos/<date>-<slug>/`. Studio opened against the repo shows every past video in one sidebar.

## Setup

1. **Install Archon** — see https://archon.diy/docs
2. **Install Claude Code** — `curl -fsSL https://claude.ai/install.sh | bash`
3. **Install the Remotion skill**, from this repo root:
   ```bash
   npx skills add remotion-dev/skills --yes
   ```
4. **System deps:** Node 20+, pnpm (`npm i -g pnpm`), Python 3.11+ with uv (`curl -LsSf https://astral.sh/uv/install.sh | sh`), `jq`, `ffmpeg`.
5. **API keys in `.archon/.env`** — at least one TTS provider:
   ```
   CARTESIA_API_KEY=sk_car_...       # voice (recommended, free tier works)
   ELEVENLABS_API_KEY=sk_...          # voice + SFX + music (music needs paid tier)
   ```

## Run

```bash
archon workflow run remotion-from-hn --no-worktree ""
archon workflow run remotion-from-hn --no-worktree "marketing https://your-site.com"
archon workflow run remotion-from-hn --no-worktree "article https://some-blog.com/post"
```

First run scaffolds the Remotion project into the repo automatically. Subsequent runs detect the existing project and skip scaffolding.

## Optional env

| Variable | Purpose |
|---|---|
| `VOICE_PROVIDER=cartesia\|elevenlabs\|none` | Force TTS provider (default: auto-detect) |
| `SFX_PROVIDER=elevenlabs` | Opt in to sound effects |
| `MUSIC_PROVIDER=elevenlabs` | Opt in to background music (paid ElevenLabs) |
| `RENDER_ENABLED=false` | Skip mp4 render + archive |
| `CLAUDE_BIN_PATH=/path/to/claude` | If Archon can't find Claude Code |

## Output

- **mp4 archive:** `./videos/<YYYY-MM-DD>-<slug>/<slug>.mp4` (gitignored)
- **Composition source:** `./src/<CompositionId>/` (committable — grows over time)
- **Audio assets:** `./public/{voiceover,music,sfx}/...` (gitignored)
- **Preview:** `npx remotion studio` — all past compositions in one Studio session

## Optional: brand overlay

Copy `.archon/brand.example.yaml` → `.archon/brand.yaml` and edit palette, font, logo watermark, and voice/music tone. Missing file = neutral defaults.
