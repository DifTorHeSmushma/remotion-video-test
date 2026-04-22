"""
YouTube video upload with metadata extraction from composition artifacts.
Supports dry-run preview, scheduled publishing, and thumbnail prompt generation.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from youtube_auth import build_youtube_client, get_credentials

load_dotenv()

# Default settings from environment
DEFAULT_PRIVACY = os.getenv('YOUTUBE_DEFAULT_PRIVACY', 'private')
DEFAULT_CATEGORY = os.getenv('YOUTUBE_DEFAULT_CATEGORY', '28')  # Science & Technology
NOTIFY_SUBSCRIBERS = os.getenv('YOUTUBE_NOTIFY_SUBSCRIBERS', 'true').lower() == 'true'
CONTAINS_SYNTHETIC_MEDIA = os.getenv('YOUTUBE_CONTAINS_SYNTHETIC_MEDIA', 'true').lower() == 'true'


@dataclass
class VideoMetadata:
    """Video metadata for YouTube upload."""
    title: str
    description: str
    tags: list[str] = field(default_factory=list)
    category_id: str = DEFAULT_CATEGORY
    privacy_status: str = DEFAULT_PRIVACY
    publish_at: Optional[str] = None  # ISO 8601 for scheduled
    notify_subscribers: bool = NOTIFY_SUBSCRIBERS
    made_for_kids: bool = False
    contains_synthetic_media: bool = CONTAINS_SYNTHETIC_MEDIA
    embeddable: bool = True
    public_stats_viewable: bool = True
    default_language: str = 'en'


def humanize_name(name: str) -> str:
    """Convert AnimationName to human-readable title."""
    # Split on capital letters and numbers
    words = re.sub(r'([A-Z])', r' \1', name).strip()
    # Handle numbers with units (5Min -> 5 Min)
    words = re.sub(r'(\d+)([A-Za-z])', r'\1 \2', words)
    return words


def extract_title(animation_name: str, src_dir: Path) -> str:
    """
    Extract video title from composition artifacts.

    Priority:
    1. content-brief.md first heading or "Core Value Proposition"
    2. youtube-description.md first line (if not generic)
    3. Humanized animation name
    """
    # Try content-brief.md
    brief_path = src_dir / 'research' / 'content-brief.md'
    if brief_path.exists():
        content = brief_path.read_text(encoding='utf-8')

        # Look for "Core Value Proposition" section
        cvp_match = re.search(r'(?:Core Value Proposition|Value Proposition)[:\s]*\n+([^\n]+)', content, re.IGNORECASE)
        if cvp_match:
            return cvp_match.group(1).strip().strip('*').strip()

        # Look for first H1 or H2
        heading_match = re.search(r'^#{1,2}\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            heading = heading_match.group(1).strip()
            if len(heading) > 10:  # Avoid generic headings
                return heading

    # Try youtube-description.md first line
    desc_path = src_dir / 'youtube-description.md'
    if desc_path.exists():
        first_line = desc_path.read_text(encoding='utf-8').split('\n')[0].strip()
        if first_line and not first_line.startswith('#') and len(first_line) > 20:
            # Truncate if too long
            if len(first_line) > 100:
                first_line = first_line[:97] + '...'
            return first_line

    # Fallback: humanize animation name
    return humanize_name(animation_name)


def extract_description(src_dir: Path) -> str:
    """Read description from youtube-description.md."""
    desc_path = src_dir / 'youtube-description.md'
    if not desc_path.exists():
        raise FileNotFoundError(f"YouTube description not found: {desc_path}")

    return desc_path.read_text(encoding='utf-8')


def extract_tags(description: str) -> list[str]:
    """
    Extract tags from description hashtags.

    Looks for lines with hashtags and extracts them.
    Also adds default channel tags.
    """
    tags = []

    # Find hashtag lines
    hashtag_pattern = re.compile(r'#(\w+)')
    matches = hashtag_pattern.findall(description)
    tags.extend(matches)

    # Add default tags if not present
    defaults = ['DIYSmartCode', 'TechTutorial']
    for tag in defaults:
        if tag not in tags:
            tags.append(tag)

    # YouTube limit: 500 chars total for tags
    # Trim if necessary
    total_chars = sum(len(t) for t in tags)
    while total_chars > 450 and tags:
        removed = tags.pop()
        total_chars -= len(removed)

    return tags


def extract_chapters(timing_file: Path) -> str:
    """
    Parse SCENES object from timing.ts and convert to YouTube chapters.

    Returns chapter text to append to description if not already present.
    """
    if not timing_file.exists():
        return ""

    content = timing_file.read_text(encoding='utf-8')

    # Parse SCENES object
    scenes_match = re.search(r'export const SCENES\s*=\s*\{([^}]+)\}', content, re.DOTALL)
    if not scenes_match:
        return ""

    scenes_content = scenes_match.group(1)

    # Extract scene names and start times
    scene_pattern = re.compile(r'(\w+):\s*\{\s*start:\s*(\d+)')
    chapters = []

    for match in scene_pattern.finditer(scenes_content):
        name = match.group(1)
        start_frames = int(match.group(2))

        # Convert frames to MM:SS (assuming 30fps)
        seconds = start_frames // 30
        minutes = seconds // 60
        secs = seconds % 60

        # Humanize scene name
        display_name = humanize_name(name)
        if display_name.lower() == 'hook':
            display_name = 'Introduction'

        chapters.append(f"{minutes}:{secs:02d} {display_name}")

    if not chapters:
        return ""

    # Ensure first chapter starts at 0:00
    if not chapters[0].startswith('0:00'):
        chapters[0] = '0:00 ' + chapters[0].split(' ', 1)[1]

    return '\n'.join(chapters)


def generate_thumbnail_prompts(animation_name: str, title: str, src_dir: Path) -> str:
    """
    Generate 5 AI image prompts for thumbnail creation.

    Returns markdown content for thumbnail-prompts.md
    """
    # Try to get core concept from content-brief
    concept = title
    brief_path = src_dir / 'research' / 'content-brief.md'
    if brief_path.exists():
        content = brief_path.read_text(encoding='utf-8')
        # Look for key concept or hook
        hook_match = re.search(r'(?:Hook|Core Concept|Key Point)[:\s]*\n+([^\n]+)', content, re.IGNORECASE)
        if hook_match:
            concept = hook_match.group(1).strip()

    prompts = f"""# Thumbnail Prompts for {animation_name}

Based on: {title}
Core concept: {concept}

---

## Prompt 1: Tech Futuristic

A sleek futuristic digital interface displaying "{title[:30]}..." with glowing blue and purple neon accents, holographic elements floating in a dark tech environment, cinematic lighting, 8K ultra-detailed, professional YouTube thumbnail style, bold readable text overlay space on the right

## Prompt 2: Before/After Split

Split-screen composition: left side shows a frustrated developer at a cluttered desk with red warning icons (labeled "BEFORE"), right side shows the same developer confident with clean code and green checkmarks (labeled "AFTER"), dramatic lighting contrast, YouTube thumbnail format, space for bold text

## Prompt 3: Bold Iconic

A powerful central icon representing {concept[:50]}... surrounded by dynamic energy waves and particles, dark gradient background transitioning from deep blue to black, minimalist design with high contrast, professional tech tutorial thumbnail, large empty space for text overlay

## Prompt 4: Minimalist Contrast

Clean white background with a single striking visual element related to "{concept[:30]}...", strong shadow casting to the right, one accent color (electric blue or orange), Apple-style minimalism, ultra-clean composition, YouTube thumbnail dimensions with text space

## Prompt 5: Dramatic Lighting

Close-up of hands typing on a keyboard with dramatic rim lighting, screen glow illuminating the scene in cool blue tones, code reflections visible, cinematic depth of field, moody tech atmosphere, professional quality suitable for YouTube thumbnail with text overlay area

---

## Usage Notes

1. Generate images at 1280x720 (YouTube thumbnail size)
2. Leave space on right side for text overlay
3. Add video title text in Canva/Photoshop after generation
4. Use bold, readable fonts (Impact, Montserrat Bold)
5. Keep text to 3-5 words maximum
"""

    return prompts


def upload_video(
    youtube_client,
    video_path: Path,
    metadata: VideoMetadata
) -> dict:
    """
    Upload video to YouTube using resumable upload.

    Args:
        youtube_client: Authenticated YouTube API client
        video_path: Path to video file
        metadata: Video metadata

    Returns:
        YouTube video resource with ID and URL
    """
    # Build request body
    body = {
        'snippet': {
            'title': metadata.title[:100],  # YouTube limit
            'description': metadata.description[:5000],  # YouTube limit
            'tags': metadata.tags,
            'categoryId': metadata.category_id,
            'defaultLanguage': metadata.default_language
        },
        'status': {
            'privacyStatus': metadata.privacy_status,
            'embeddable': metadata.embeddable,
            'publicStatsViewable': metadata.public_stats_viewable,
            'selfDeclaredMadeForKids': metadata.made_for_kids,
            'containsSyntheticMedia': metadata.contains_synthetic_media
        }
    }

    # Add scheduled publish time if specified
    if metadata.publish_at and metadata.privacy_status == 'private':
        body['status']['publishAt'] = metadata.publish_at
        body['status']['privacyStatus'] = 'private'  # Must be private for scheduling

    # Create media upload
    media = MediaFileUpload(
        str(video_path),
        mimetype='video/mp4',
        resumable=True,
        chunksize=1024 * 1024 * 10  # 10MB chunks
    )

    # Execute upload with progress
    request = youtube_client.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media,
        notifySubscribers=metadata.notify_subscribers
    )

    response = None
    file_size = video_path.stat().st_size
    print(f"\n[4/5] Uploading video...")

    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            uploaded = int(status.resumable_progress / (1024 * 1024))
            total = int(file_size / (1024 * 1024))
            bar_width = 30
            filled = int(bar_width * status.progress())
            bar = '=' * filled + '-' * (bar_width - filled)
            print(f"      |{bar}| {progress}% ({uploaded} MB / {total} MB)", end='\r')

    print()  # New line after progress
    return response


def dry_run(metadata: VideoMetadata, video_path: Path, chapters: str) -> None:
    """Preview upload metadata without making API calls."""
    file_size_mb = video_path.stat().st_size / (1024 * 1024)

    print("\n" + "=" * 50)
    print("YouTube Upload Preview (DRY RUN)")
    print("=" * 50)

    print(f"\nVideo File: {video_path}")
    print(f"File Size: {file_size_mb:.1f} MB")

    print(f"\nTitle: {metadata.title}")

    print(f"\nDescription ({len(metadata.description)} chars):")
    preview = metadata.description[:500]
    if len(metadata.description) > 500:
        preview += "\n[... truncated]"
    print(preview)

    print(f"\nTags ({len(metadata.tags)}): {', '.join(metadata.tags[:10])}")
    if len(metadata.tags) > 10:
        print(f"      ... and {len(metadata.tags) - 10} more")

    print(f"\nCategory: {metadata.category_id} (Science & Technology)")
    print(f"Privacy: {metadata.privacy_status}")
    if metadata.publish_at:
        print(f"Scheduled: {metadata.publish_at}")

    print(f"\nAI Disclosure: {'Yes' if metadata.contains_synthetic_media else 'No'}")
    print(f"Subscriber Notification: {'Yes' if metadata.notify_subscribers else 'No'}")
    print(f"Made for Kids: {'Yes' if metadata.made_for_kids else 'No'}")

    if chapters:
        print(f"\nChapters (from timing.ts):")
        for line in chapters.split('\n')[:5]:
            print(f"  {line}")
        if chapters.count('\n') > 4:
            print(f"  ... and {chapters.count(chr(10)) - 4} more")

    print("\n" + "=" * 50)
    print("To upload for real, remove --dry-run flag.")
    print("=" * 50 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description='Upload video to YouTube with auto-extracted metadata'
    )
    parser.add_argument(
        'animation_name',
        help='Animation folder name (e.g., DockerSandboxes5Min)'
    )
    parser.add_argument(
        '--privacy',
        choices=['public', 'unlisted', 'private'],
        default=DEFAULT_PRIVACY,
        help=f'Privacy setting (default: {DEFAULT_PRIVACY})'
    )
    parser.add_argument(
        '--schedule',
        help='ISO 8601 datetime for scheduled publish (e.g., 2026-01-28T15:00:00Z)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview metadata without uploading'
    )
    parser.add_argument(
        '--no-notify',
        action='store_true',
        help='Disable subscriber notifications'
    )
    parser.add_argument(
        '--title',
        help='Override auto-generated title'
    )
    parser.add_argument(
        '--tags',
        help='Additional comma-separated tags'
    )
    parser.add_argument(
        '--gen-thumbs',
        action='store_true',
        help='Generate thumbnail-prompts.md for AI image tools'
    )

    args = parser.parse_args()

    # Resolve paths
    animation_name = args.animation_name
    src_dir = Path(f'src/{animation_name}')
    video_path = Path(f'out/{animation_name}/final.mp4')
    timing_file = src_dir / 'constants' / 'timing.ts'

    print(f"\nYouTube Upload: {animation_name}")
    print("=" * 50)

    # Step 1: Validate prerequisites
    print("\n[1/5] Validating prerequisites...")

    if not src_dir.exists():
        print(f"Error: Source directory not found: {src_dir}")
        sys.exit(1)

    if not video_path.exists() and not args.dry_run and not args.gen_thumbs:
        print(f"Error: Video file not found: {video_path}")
        print("Run Phase 5 first to render the video.")
        sys.exit(1)

    desc_path = src_dir / 'youtube-description.md'
    if not desc_path.exists():
        print(f"Error: YouTube description not found: {desc_path}")
        print("Run Phase 5 first to generate the description.")
        sys.exit(1)

    print("  Prerequisites OK")

    # Step 2: Extract metadata
    print("\n[2/5] Extracting metadata...")

    title = args.title or extract_title(animation_name, src_dir)
    description = extract_description(src_dir)
    tags = extract_tags(description)
    chapters = extract_chapters(timing_file)

    # Add extra tags from CLI
    if args.tags:
        extra_tags = [t.strip() for t in args.tags.split(',')]
        tags = extra_tags + tags

    print(f"  Title: {title[:50]}...")
    print(f"  Description: {len(description)} chars")
    print(f"  Tags: {len(tags)} tags")
    print(f"  Chapters: {chapters.count(chr(10)) + 1 if chapters else 0} chapters")

    # Step 3: Generate thumbnail prompts if requested
    if args.gen_thumbs:
        print("\n[3/5] Generating thumbnail prompts...")
        prompts = generate_thumbnail_prompts(animation_name, title, src_dir)
        prompts_path = src_dir / 'thumbnail-prompts.md'
        prompts_path.write_text(prompts, encoding='utf-8')
        print(f"  Saved to: {prompts_path}")

    # Build metadata object
    metadata = VideoMetadata(
        title=title,
        description=description,
        tags=tags,
        privacy_status=args.privacy,
        publish_at=args.schedule,
        notify_subscribers=not args.no_notify
    )

    # Step 4: Dry run or upload
    if args.dry_run:
        # Use a dummy path for dry run if video doesn't exist
        if video_path.exists():
            dry_run(metadata, video_path, chapters)
        else:
            print("\n[DRY RUN] Video file not found, showing metadata only:")
            print(f"\nTitle: {metadata.title}")
            print(f"Privacy: {metadata.privacy_status}")
            print(f"Tags: {', '.join(metadata.tags[:5])}...")
        return

    if args.gen_thumbs and not video_path.exists():
        print("\n[5/5] Thumbnail prompts generated. Skipping upload (no video).")
        return

    # Step 3b: Authenticate
    print("\n[3/5] Authenticating...")
    try:
        youtube = build_youtube_client()
        print("  Authenticated (cached token)")
    except FileNotFoundError:
        print("  Authentication setup required. See instructions above.")
        sys.exit(1)
    except Exception as e:
        print(f"  Authentication failed: {e}")
        sys.exit(1)

    # Step 4: Upload
    try:
        response = upload_video(youtube, video_path, metadata)

        video_id = response['id']
        video_url = f"https://youtube.com/watch?v={video_id}"

        print("\n[5/5] Upload complete!")
        print(f"\nVideo URL: {video_url}")
        print(f"Video ID: {video_id}")
        print(f"Status: Processing (check back in ~5 minutes)")
        print(f"Privacy: {metadata.privacy_status}")

        if metadata.publish_at:
            print(f"Scheduled: {metadata.publish_at}")

        print("\nNext steps:")
        print("- Change privacy to 'public' when ready to publish")
        print("- Add to playlist: Studio > Content > Select video > Add to playlist")
        print("- Add end screen: Studio > Content > Details > End screen")
        print("- Verify chapters appear correctly (may need page refresh)")

    except HttpError as e:
        if e.resp.status == 403:
            print(f"\nError: API quota exceeded or insufficient permissions")
            print("Daily quota resets at midnight Pacific Time")
        elif e.resp.status == 400:
            error_details = json.loads(e.content)
            print(f"\nError: Invalid metadata")
            print(json.dumps(error_details, indent=2))
        else:
            print(f"\nUpload failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
