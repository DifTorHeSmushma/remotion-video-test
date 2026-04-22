---
description: "Phase 6: Upload rendered video to YouTube with auto-extracted metadata"
argument-hint: <AnimationName (folder name under src/)>
---

<objective>
Execute Phase 6 of the DIY YouTube Video Creation Workflow.
Upload the rendered video for "$ARGUMENTS" to YouTube.

**Goal**: Upload the final video with properly formatted metadata, chapters, and AI disclosures.
**Input**:
  - `out/$ARGUMENTS/final.mp4` (from Phase 5)
  - `src/$ARGUMENTS/youtube-description.md` (from Phase 5)
  - `src/$ARGUMENTS/constants/timing.ts` (for chapters)
**Output**: Published/scheduled YouTube video with URL
**Reference**: YouTube Data API v3
</objective>

<process>

### Phase Gate

Read `src/$ARGUMENTS/phase-status.md` (if it exists).
- **Prerequisites**: Verify Phase 5 (Render) is `done`.
  - If not: STOP and report "Phase 5 (Render) has not been completed. Run `/diy-yt-creation:phase5-render $ARGUMENTS` first."
- **Re-run check**: If Phase 6-Upload is already `done`, warn the user before overwriting.
  In autonomous mode (full-auto), skip the warning and proceed.

## Step 1: Verify Prerequisites

Check that the following files exist:
1. `out/$ARGUMENTS/final.mp4` - Rendered video
2. `src/$ARGUMENTS/youtube-description.md` - Video description
3. `client_secrets.json` - OAuth credentials (project root)

If `client_secrets.json` is missing, display setup instructions:

```
SETUP REQUIRED: YouTube API credentials

1. Go to https://console.cloud.google.com
2. Create a new project (or select existing)
3. Enable 'YouTube Data API v3':
   - APIs & Services > Library > search 'YouTube Data API v3'
4. Create OAuth credentials:
   - APIs & Services > Credentials > Create Credentials
   - Select 'OAuth client ID' > 'Desktop app'
5. Download the JSON file
6. Save it as 'client_secrets.json' in the project root
```

## Step 2: Generate Thumbnail Prompts

Generate AI image prompts for thumbnail creation:

```bash
python youtube_upload.py $ARGUMENTS --gen-thumbs --dry-run
```

This creates `src/$ARGUMENTS/thumbnail-prompts.md` with 5 prompts for tools like Nana/Banana.

Inform the user they can create thumbnails using these prompts and upload manually via YouTube Studio.

## Step 3: Preview Upload (Dry Run)

Run dry-run to verify all metadata before uploading:

```bash
python youtube_upload.py $ARGUMENTS --dry-run
```

Review the output with user:
- Is the title correct? (Can override with `--title "Custom Title"`)
- Is the description complete with chapters?
- Are tags appropriate?
- Is AI disclosure enabled?

## Step 4: Select Privacy Setting

Ask user which privacy level to use:

| Setting | Description |
|---------|-------------|
| `private` (default) | Only you can view. Safest option. |
| `unlisted` | Anyone with link can view. Good for review. |
| `public` | Discoverable by anyone. Ready to publish. |

For scheduled publishing (publishes at specified time):
```bash
python youtube_upload.py $ARGUMENTS --privacy private --schedule "2026-01-28T15:00:00Z"
```

## Step 5: Upload Video

Execute the upload with selected privacy:

```bash
python youtube_upload.py $ARGUMENTS --privacy <selected>
```

Additional options:
- `--no-notify` - Don't notify subscribers (good for test uploads)
- `--title "Custom Title"` - Override auto-detected title
- `--tags "tag1,tag2,tag3"` - Add extra tags

Monitor upload progress:
- File size and upload percentage shown
- Handles network interruptions with resumable upload
- Reports any API errors

## Step 6: Post-Upload Verification

After successful upload:

1. **Display Results**:
   - Video URL: `https://youtube.com/watch?v=<VIDEO_ID>`
   - Video ID for reference
   - Current processing status

2. **Remind User to Complete**:
   - Upload thumbnail via YouTube Studio
   - Add to relevant playlists
   - Add end screen elements (subscribe button, related videos)
   - Add cards linking to other content
   - Verify chapters appear correctly (may need page refresh)

3. **If Privacy is Private**:
   - Remind user to change to 'public' when ready
   - Or use `--schedule` next time for automatic publishing

</process>

<output>
**Files created/used**:
- `src/$ARGUMENTS/thumbnail-prompts.md` (new)
- `out/$ARGUMENTS/final.mp4` (uploaded)
- `src/$ARGUMENTS/youtube-description.md` (used for metadata)

**Report to user**:
1. Upload status (success/failure)
2. Video URL (even for private videos)
3. Video ID
4. Processing status
5. Thumbnail prompts location
6. Next steps checklist:
   - [ ] Create and upload thumbnail
   - [ ] Add to playlist
   - [ ] Add end screen
   - [ ] Add cards
   - [ ] Verify chapters
   - [ ] Change privacy when ready

**Workflow Complete!** The video creation pipeline is finished.

### Update Phase Status

Update `src/$ARGUMENTS/phase-status.md` — set the `6 - Upload` row to `done` with today's date. If the file doesn't exist, create it with all phases as `pending` first (see Phase 0 template).
</output>
