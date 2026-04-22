---
description: "Restore an archived video composition from src/_archived/"
argument-hint: <CompositionName (folder name under src/_archived/)>
---

<objective>
Restore an archived video composition "$ARGUMENTS" for re-rendering or editing.

**Goal**: Move composition back from archive, uncomment in Root.tsx
**Input**: Composition name (e.g., "ClaudeCodeV2119", "ExcalidrawSkill")
**Output**: Files restored to `src/`, imports active in Root.tsx
</objective>

<process>

## Step 1: Validate Archived Composition Exists

Check that the archived folder exists:
```
src/_archived/$ARGUMENTS/
```

If not found, list available archived compositions:
```bash
ls src/_archived/
```

## Step 2: Move Composition Folder Back

```bash
mv src/_archived/$ARGUMENTS src/$ARGUMENTS
```

## Step 3: Check for Related Shorts

Check if archived Shorts folder exists:
```
src/_archived/$ARGUMENTSShorts/
```

If found, move it too:
```bash
mv src/_archived/$ARGUMENTSShorts src/$ARGUMENTSShorts
```

## Step 4: Restore Audio Files

Check if archived audio exists:
```
public/audio/_archived/<lowercase-name>/
```

If found, move back:
```bash
mv public/audio/_archived/<lowercase-name> public/audio/<lowercase-name>
```

## Step 5: Update Root.tsx

Uncomment the imports and Composition registration.

### 5.1 Uncomment Imports

Find lines with `// ARCHIVED: import` for this composition and remove the comment prefix.

### 5.2 Uncomment Composition Registration

Find the commented `{/* ARCHIVED: <Composition id="$ARGUMENTS" ... */ }` block and uncomment it.

### 5.3 Handle Related Shorts

If Shorts were restored, also uncomment their imports and registrations.

### 5.4 Add to Review Webapp (Optional)

If you want the composition available in the review webapp, add it to `apps/review-webapp/src/lib/compositions.ts`:

1. Add import statements for the composition and timing constants
2. Add an entry to the `COMPOSITIONS` object

## Step 6: Verify Build

```bash
pnpm lint
```

## Step 7: Test in Studio

```bash
pnpm dev
```

Confirm composition appears in Remotion Studio sidebar.

</process>

<output>
Confirm to user:
1. What was restored from `src/_archived/`
2. What was uncommented in Root.tsx
3. Build verification status
4. Composition is ready for preview/render
</output>
