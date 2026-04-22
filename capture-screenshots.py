"""
Batch screenshot capture for video compositions via agent-browser.

Usage:
  python capture-screenshots.py <AnimationName>                    # Capture all
  python capture-screenshots.py <AnimationName> --name <name>      # Capture single
  python capture-screenshots.py <AnimationName> --dry-run          # Preview commands
  python capture-screenshots.py <AnimationName> --force            # Re-capture existing

Example:
  python capture-screenshots.py BrowserE2eToolsCompared
  python capture-screenshots.py BrowserE2eToolsCompared --name playwright-docs --dry-run

This reads the screenshot manifest from src/<AnimationName>/images/screenshots.json
and captures all specified screenshots to public/images/<animationname>/.

Manifest format:
{
  "composition": "AnimationName",
  "defaults": {
    "viewport": [1920, 1080],
    "color_scheme": "dark",
    "wait_strategy": "networkidle",
    "delay_after_load_ms": 1500
  },
  "screenshots": [
    {
      "name": "github-repo-hero",
      "url": "https://github.com/org/repo",
      "scene": "scene03",
      "usage": "Product intro background",
      "color_scheme": "dark"
    }
  ]
}
"""

import os
import sys
import argparse

from screenshot_capture_lib import (
    load_manifest,
    capture_screenshot,
    open_browser_session,
    close_browser_session,
)


def main():
    parser = argparse.ArgumentParser(
        description="Capture website screenshots for a video composition"
    )
    parser.add_argument(
        "animation_name",
        help="Animation name (folder name under src/)",
    )
    parser.add_argument(
        "--name",
        help="Capture only the screenshot with this name",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview commands without capturing",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-capture even if output file already exists",
    )

    args = parser.parse_args()
    animation_name = args.animation_name

    # Locate manifest
    manifest_path = os.path.join("src", animation_name, "images", "screenshots.json")
    output_dir = os.path.join("public", "images", animation_name.lower())

    if not os.path.isfile(manifest_path):
        print(f"Error: Screenshot manifest not found at {manifest_path}")
        print(
            f"\nTo create a manifest, add src/{animation_name}/images/screenshots.json:"
        )
        print(
            """
{
  "composition": "%s",
  "defaults": {
    "viewport": [1920, 1080],
    "color_scheme": "dark",
    "wait_strategy": "networkidle",
    "delay_after_load_ms": 1500
  },
  "screenshots": [
    {
      "name": "example-hero",
      "url": "https://example.com",
      "scene": "scene01",
      "usage": "Hero background"
    }
  ]
}
"""
            % animation_name
        )
        sys.exit(1)

    # Load manifest
    print(f"Reading manifest: {manifest_path}")
    defaults, entries = load_manifest(manifest_path)

    # Filter to single entry if --name specified
    if args.name:
        entries = [e for e in entries if e.name == args.name]
        if not entries:
            print(f"Error: No screenshot named '{args.name}' in manifest")
            sys.exit(1)

    # Override skip_if_exists when --force
    if args.force:
        for entry in entries:
            entry.skip_if_exists = False

    print(f"Output directory: {output_dir}")
    print(f"Screenshots to capture: {len(entries)}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE CAPTURE'}")
    print()

    # Ensure output dir exists
    os.makedirs(output_dir, exist_ok=True)

    # Open browser session (unless dry run)
    if not args.dry_run:
        print("Starting browser session...")
        if not open_browser_session():
            print("Warning: Could not verify browser session, proceeding anyway...")
        print()

    # Capture each screenshot
    results = []
    succeeded = 0
    skipped = 0
    failed = 0

    try:
        for i, entry in enumerate(entries, 1):
            print(f"Screenshot {i}/{len(entries)}: {entry.name}")
            print(f"  URL: {entry.url}")
            if entry.scene:
                print(f"  Scene: {entry.scene}")
            if entry.usage:
                print(f"  Usage: {entry.usage}")

            result = capture_screenshot(entry, output_dir, dry_run=args.dry_run)
            results.append(result)

            if result.success:
                if result.error and "Skipped" in result.error:
                    print(f"  Status: SKIPPED (already exists, {result.file_size_kb:.0f}KB)")
                    print(f"  Remotion: staticFile('{result.staticfile_path}')")
                    skipped += 1
                elif result.error and "Dry run" in result.error:
                    print(f"  Status: DRY RUN OK")
                    succeeded += 1
                else:
                    print(f"  Output: {result.output_path} ({result.file_size_kb:.0f}KB)")
                    print(f"  Remotion: staticFile('{result.staticfile_path}')")
                    print(f"  Status: OK (attempt {result.attempts})")
                    succeeded += 1
            else:
                print(f"  Status: FAILED after {result.attempts} attempts")
                print(f"  Error: {result.error}")
                failed += 1

            print()
    finally:
        # Always close browser
        if not args.dry_run:
            print("Closing browser session...")
            close_browser_session()

    # Summary
    print("=" * 60)
    print(f"Summary: {succeeded} captured, {skipped} skipped, {failed} failed")
    print(f"Total:   {len(entries)} screenshots")
    print()

    if failed > 0:
        print("Failed screenshots (may need manual capture):")
        for r in results:
            if not r.success:
                print(f"  - {r.name}: {r.error}")
                print(f"    URL: {r.url}")
        print()

    # Print Remotion import reference
    if succeeded > 0 or skipped > 0:
        print("Remotion usage (copy-paste into scenes):")
        print()
        for r in results:
            if r.success:
                print(f"  // {r.name} ({r.usage if hasattr(r, 'usage') else ''})")
                print(f"  staticFile('{r.staticfile_path}')")
                print()

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
