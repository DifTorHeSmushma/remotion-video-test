"""
Generate a single YouTube thumbnail using Replicate AI models.

Usage:
  # From composition with style
  python generate-thumbnail.py --composition MyVideoName --style tech-dramatic

  # From manifest file
  python generate-thumbnail.py --manifest src/MyVideo/thumbnails/manifest.json

  # Direct prompt
  python generate-thumbnail.py -p "prompt" -o public/thumbnails/ -n thumb-name

  # With face reference (for consistent identity)
  python generate-thumbnail.py -c MyVideo --face-ref public/reference-faces/creator/

Examples:
  python generate-thumbnail.py \\
    --composition ClaudeCodeV2120 \\
    --style tech-dramatic \\
    --concept "AI coding assistant with glowing terminal interface"

  python generate-thumbnail.py \\
    --manifest src/ClaudeCodeV2120/thumbnails/manifest.json

  python generate-thumbnail.py \\
    -p "Futuristic AI assistant helping developer" \\
    -o public/thumbnails/test/ \\
    -n my-thumbnail \\
    --style minimalist

  # With face reference
  python generate-thumbnail.py \\
    -c MyVideo \\
    --concept "Tech expert explaining AI" \\
    --face-ref public/reference-faces/creator/ \\
    --expression excited \\
    --face-weight 0.85
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from thumbnail_lib import (
    ThumbnailSpec,
    ThumbnailWithFaceSpec,
    generate_thumbnail,
    generate_thumbnail_with_face,
    load_manifest,
    get_style_info,
    get_model_info,
    get_face_model_info,
    STYLE_PRESETS,
    MODELS,
    FACE_REF_MODELS,
    DEFAULT_STYLE,
    DEFAULT_FACE_MODEL,
    DEFAULT_FACE_WEIGHT,
)

load_dotenv()


def list_styles():
    """Print available style presets."""
    print("\nAvailable Style Presets:")
    print("-" * 60)
    for style_id, info in STYLE_PRESETS.items():
        print(f"\n  {style_id}")
        print(f"    Description: {info['description']}")
        print(f"    Best for: {info['best_for']}")
        print(f"    Recommended model: {info['recommended_model']}")
    print()


def list_models():
    """Print available models."""
    print("\nAvailable Models:")
    print("-" * 60)
    for model_id, info in MODELS.items():
        print(f"\n  {model_id}")
        print(f"    Name: {info['name']}")
        print(f"    Cost: ${info['cost_per_image']:.3f}/image")
        print(f"    Text rendering: {info['text_rendering']}")
        print(f"    Best for: {info['best_for']}")
    print()


def list_face_models():
    """Print available face reference models."""
    print("\nAvailable Face Reference Models:")
    print("-" * 60)
    for model_id, info in FACE_REF_MODELS.items():
        print(f"\n  {model_id}")
        print(f"    Name: {info['name']}")
        print(f"    Cost: ${info['cost_per_image']:.3f}/image")
        print(f"    Consistency: {info['face_consistency']}")
        print(f"    Best for: {info['best_for']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Generate a YouTube thumbnail using Replicate AI models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate from composition
  python generate-thumbnail.py --composition MyVideo --style tech-dramatic

  # Generate from manifest
  python generate-thumbnail.py --manifest src/MyVideo/thumbnails/manifest.json

  # Direct prompt
  python generate-thumbnail.py -p "AI robot coding" -o public/thumbnails/ -n test
        """,
    )

    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--composition", "-c",
        help="Composition name (uses default thumbnail dir and manifest if exists)"
    )
    mode_group.add_argument(
        "--manifest", "-m",
        help="Path to thumbnail manifest JSON file"
    )
    mode_group.add_argument(
        "--prompt", "-p",
        help="Direct prompt for image generation"
    )
    mode_group.add_argument(
        "--list-styles",
        action="store_true",
        help="List available style presets"
    )
    mode_group.add_argument(
        "--list-models",
        action="store_true",
        help="List available AI models"
    )
    mode_group.add_argument(
        "--list-face-models",
        action="store_true",
        help="List available face reference models"
    )

    # Direct prompt options
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory (required for --prompt mode)"
    )
    parser.add_argument(
        "--name", "-n",
        help="Output filename without extension (required for --prompt mode)"
    )

    # Common options
    parser.add_argument(
        "--style", "-s",
        default=DEFAULT_STYLE,
        choices=list(STYLE_PRESETS.keys()),
        help=f"Style preset (default: {DEFAULT_STYLE})"
    )
    parser.add_argument(
        "--concept",
        help="Visual concept description (overrides manifest)"
    )
    parser.add_argument(
        "--model",
        choices=list(MODELS.keys()),
        help="AI model to use (default: auto-selected based on style)"
    )
    parser.add_argument(
        "--format", "-f",
        default="png",
        choices=["jpg", "png"],
        help="Output format (default: png)"
    )
    parser.add_argument(
        "--text-position",
        choices=["left", "right", "top", "bottom"],
        help="Reserve space for text overlay"
    )

    # Face reference options
    parser.add_argument(
        "--face-ref",
        help="Path to directory with face reference images"
    )
    parser.add_argument(
        "--face-url",
        help="Direct URL to face reference image"
    )
    parser.add_argument(
        "--face-model",
        choices=list(FACE_REF_MODELS.keys()),
        default=DEFAULT_FACE_MODEL,
        help=f"Face reference model (default: {DEFAULT_FACE_MODEL})"
    )
    parser.add_argument(
        "--face-weight",
        type=float,
        default=DEFAULT_FACE_WEIGHT,
        help=f"Face preservation strength 0.01-2 (default: {DEFAULT_FACE_WEIGHT})"
    )
    parser.add_argument(
        "--expression",
        choices=["excited", "smile", "serious", "surprised", "thoughtful"],
        help="Desired facial expression"
    )

    args = parser.parse_args()

    # Handle list commands
    if args.list_styles:
        list_styles()
        return 0

    if args.list_models:
        list_models()
        return 0

    if args.list_face_models:
        list_face_models()
        return 0

    # Validate arguments
    if args.prompt:
        if not args.output_dir or not args.name:
            print("Error: --output-dir and --name are required when using --prompt", file=sys.stderr)
            return 1

    if not args.composition and not args.manifest and not args.prompt:
        print("Error: Must specify --composition, --manifest, or --prompt", file=sys.stderr)
        parser.print_help()
        return 1

    # Build ThumbnailSpec
    try:
        if args.manifest:
            # Load from manifest file
            spec = load_manifest(args.manifest)
            output_dir = os.path.dirname(args.manifest)
            name = spec.composition or "thumbnail"

        elif args.composition:
            # Try to load manifest, or create spec from arguments
            manifest_path = f"src/{args.composition}/thumbnails/manifest.json"
            if os.path.exists(manifest_path):
                spec = load_manifest(manifest_path)
                output_dir = os.path.dirname(manifest_path)
            else:
                # Create spec from arguments
                if not args.concept:
                    print(f"Error: No manifest found at {manifest_path}", file=sys.stderr)
                    print("Provide --concept or create a manifest file", file=sys.stderr)
                    return 1
                spec = ThumbnailSpec(
                    concept=args.concept,
                    composition=args.composition,
                    style=args.style,
                )
                output_dir = f"public/thumbnails/{args.composition.lower()}"
            name = args.composition

        else:  # args.prompt
            # Create spec from direct prompt
            text_overlay = None
            if args.text_position:
                text_overlay = {
                    "enabled": True,
                    "position": args.text_position,
                }

            spec = ThumbnailSpec(
                concept=args.prompt,
                style=args.style,
                text_overlay=text_overlay,
            )
            output_dir = args.output_dir
            name = args.name

        # Override with command line arguments
        if args.concept:
            spec.concept = args.concept
        if args.style != DEFAULT_STYLE:
            spec.style = args.style
        if args.model:
            spec.model = args.model
        if args.text_position and not spec.text_overlay:
            spec.text_overlay = {
                "enabled": True,
                "position": args.text_position,
            }

        # Build output path
        output_path = os.path.join(output_dir, f"{name.lower()}.{args.format}")

        # Generate thumbnail
        print("\n" + "=" * 60)
        print("YouTube Thumbnail Generator")
        print("=" * 60 + "\n")

        # Check if using face reference
        use_face_ref = args.face_ref or args.face_url

        if use_face_ref:
            # Create face-aware spec
            face_spec = ThumbnailWithFaceSpec(
                concept=spec.concept,
                title=spec.title,
                composition=spec.composition,
                style=spec.style,
                text_overlay=spec.text_overlay,
                brand_colors=spec.brand_colors,
                model=spec.model,
                face_ref_dir=args.face_ref,
                face_ref_url=args.face_url,
                face_model=args.face_model,
                face_weight=args.face_weight,
                expression=args.expression,
            )

            result = generate_thumbnail_with_face(
                spec=face_spec,
                output_path=output_path,
                output_format=args.format,
            )

            if result["success"]:
                print(f"\n[OK] Thumbnail saved to: {result['path']}")
                print(f"     Face model: {result['face_model']}")
                print(f"     Face weight: {result['face_weight']}")
                print(f"     Expression: {result.get('expression', 'default')}")
                print(f"     Style: {result['style']}")
                print(f"     Cost: ${result['cost']:.3f}")
                return 0
        else:
            result = generate_thumbnail(
                spec=spec,
                output_path=output_path,
                output_format=args.format,
            )

            if result["success"]:
                print(f"\n[OK] Thumbnail saved to: {result['path']}")
                print(f"     Model: {result['model']}")
                print(f"     Style: {result['style']}")
                print(f"     Cost: ${result['cost']:.3f}")
                return 0

        print("\n[FAIL] Failed to generate thumbnail", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
