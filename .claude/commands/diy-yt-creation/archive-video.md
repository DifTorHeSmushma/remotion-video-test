---
description: "Archive a published video composition to src/_archived/"
argument-hint: <CompositionName (folder name under src/)>
---

<objective>
Archive a published video composition "$ARGUMENTS" to reduce clutter in the active src/ directory.

**Goal**: Move composition folder and related assets to archive, remove from Root.tsx and review webapp
**Input**: Composition name (e.g., "ClaudeCodeV2119", "ExcalidrawSkill")
**Output**: Files moved to `src/_archived/`, all references removed from Root.tsx and review webapp
</objective>

<process>

## Step 1: Validate Composition Exists

Check that `src/$ARGUMENTS/` exists. If not found, list `src/` contents and ask user to confirm the correct name.

## Step 2: Discover All Related Folders

Scan for ALL folders that belong to this composition:

```bash
# Main composition
ls src/$ARGUMENTS/

# Related variants — check all of these patterns:
ls src/${ARGUMENTS}Shorts/ 2>/dev/null
ls src/${ARGUMENTS}TikTok/ 2>/dev/null
ls src/${ARGUMENTS}Shorts2/ 2>/dev/null
```

Note every folder found — ALL must be moved.

## Step 3: Move Composition Folders

```bash
mkdir -p src/_archived
mv src/$ARGUMENTS src/_archived/$ARGUMENTS

# Move any related folders found in Step 2:
mv src/${ARGUMENTS}Shorts src/_archived/${ARGUMENTS}Shorts       # if exists
mv src/${ARGUMENTS}TikTok src/_archived/${ARGUMENTS}TikTok       # if exists
```

## Step 4: Move Audio Files

Scan `public/audio/` for folders whose names contain the composition name (case-insensitive):

```bash
ls public/audio/ | grep -i "$ARGUMENTS"
```

Also try lowercase variants (strip hyphens, lowercase everything):
```bash
ls public/audio/ | grep -i "$(echo $ARGUMENTS | tr '[:upper:]' '[:lower:]' | tr -d '-')"
```

For EACH matching audio folder found:
```bash
mkdir -p public/audio/_archived
mv public/audio/<matching-folder> public/audio/_archived/<matching-folder>
```

Do NOT guess — only move folders that actually exist and clearly match this composition.

## Step 5: Update src/Root.tsx — Imports

Read `src/Root.tsx` and find ALL import lines that reference `$ARGUMENTS` (and its variants like `${ARGUMENTS}Shorts`, `${ARGUMENTS}TikTok`). Use grep to find them:

```bash
grep -n "$ARGUMENTS" src/Root.tsx
```

For each active (non-commented) import line found, comment it out by adding `// ARCHIVED: ` prefix:

```ts
// ARCHIVED: import { FooComposition } from "./Foo/Composition";
// ARCHIVED: import { TOTAL_FRAMES as FOO_TOTAL } from "./Foo/constants/timing";
// ARCHIVED: import { FooSchema, SCENE_KEYS as FOO_KEYS, propsToOverrides as fooPropsToOverrides } from "./Foo/schema";
```

**Also comment out any standalone utility imports only used by this composition**, such as:
- `CalculateMetadataFunction` from remotion (if only used by archived calculateMetadata)
- `computeAdjustedTiming` (if no other active compositions use it after archiving)

## Step 6: Update src/Root.tsx — Composition Registrations

Find the `<Composition id="$ARGUMENTS"` block in Root.tsx (and any related Shorts/TikTok registrations). Replace each `<Composition ... />` block with a single-line comment:

```tsx
{/* ARCHIVED: $ARGUMENTS — see src/_archived/ */}
```

**For compositions with calculateMetadata functions** (like CareerLadder): also find and wrap the entire `const calculateXxxMetadata = ...` function block in `/* ARCHIVED: ... */` comments.

## Step 7: Remove from Review Webapp

Read `apps/review-webapp/src/lib/compositions.ts`. If this composition has an entry:
1. Remove its import line
2. Remove its entry from the `COMPOSITIONS` object

## Step 8: Run Lint

```bash
pnpm lint
```

Fix any errors. Common issues:
- Unused import aliases left behind after commenting (delete the whole import line)
- `CalculateMetadataFunction` import that's now unused

## Step 9: Summary Report

Report exactly what was done:
- [ ] Folders moved: list each `src/X/ → src/_archived/X/`
- [ ] Audio moved: list each `public/audio/X/ → public/audio/_archived/X/` (or "none found")
- [ ] Root.tsx imports commented out: count of lines
- [ ] Root.tsx registrations removed: list each composition ID
- [ ] Review webapp: removed / not present
- [ ] Lint: PASS / FIXED (describe any fixes)

</process>

<restore-instructions>
## How to Restore an Archived Video

To bring back an archived composition for re-rendering or editing:

1. **Move folder back**:
   ```bash
   mv src/_archived/$ARGUMENTS src/$ARGUMENTS
   mv src/_archived/${ARGUMENTS}Shorts src/${ARGUMENTS}Shorts  # if exists
   ```

2. **Uncomment in Root.tsx**:
   - Remove `// ARCHIVED: ` prefix from all import lines
   - Replace `{/* ARCHIVED: $ARGUMENTS — see src/_archived/ */}` with the original `<Composition ... />` block (check git history for the original)

3. **Restore audio (if needed)**:
   ```bash
   mv public/audio/_archived/<name> public/audio/<name>
   ```

4. **Re-add to review webapp** if needed.

5. **Run**: `pnpm dev`
</restore-instructions>

<output>
Confirm to user:
1. All folders moved to `src/_archived/`
2. Audio moved (or not found)
3. Root.tsx — imports commented, registrations removed
4. Review webapp status
5. Lint result
</output>
