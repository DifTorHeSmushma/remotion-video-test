"""
Generate multiple YouTube thumbnail variations for A/B testing.

Usage:
  python generate-thumbnail-variations.py <CompositionName> [--count N]

Examples:
  # Generate 5 variations (default)
  python generate-thumbnail-variations.py ClaudeCodeV2120

  # Generate 3 variations
  python generate-thumbnail-variations.py ClaudeCodeV2120 --count 3

  # Custom style and output
  python generate-thumbnail-variations.py ClaudeCodeV2120 \\
    --count 5 \\
    --style tech-dramatic \\
    --output-dir public/thumbnails/test/

  # With face reference (cycles through expressions)
  python generate-thumbnail-variations.py ClaudeCodeV2120 \\
    --face-ref public/reference-faces/creator/ \\
    --count 5
"""

import os
import sys
import argparse
from dotenv import load_dotenv
from thumbnail_lib import (
    ThumbnailSpec,
    ThumbnailWithFaceSpec,
    generate_variations,
    generate_face_variations,
    load_manifest,
    STYLE_PRESETS,
    MODELS,
    FACE_REF_MODELS,
    DEFAULT_STYLE,
    DEFAULT_FACE_MODEL,
    DEFAULT_FACE_WEIGHT,
)

load_dotenv()


def main():
    parser = argparse.ArgumentParser(
        description="Generate multiple thumbnail variations for A/B testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "composition",
        help="Composition name (e.g., ClaudeCodeV2120)"
    )
    parser.add_argument(
        "--count", "-n",
        type=int,
        default=5,
        help="Number of variations to generate (default: 5)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        help="Output directory (default: public/thumbnails/<composition>/)"
    )
    parser.add_argument(
        "--style", "-s",
        default=None,
        choices=list(STYLE_PRESETS.keys()),
        help="Style preset (overrides manifest)"
    )
    parser.add_argument(
        "--concept", "-c",
        help="Visual concept (overrides manifest)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=list(MODELS.keys()),
        help="AI model to use (default: auto-selected)"
    )
    parser.add_argument(
        "--format", "-f",
        default="png",
        choices=["jpg", "png"],
        help="Output format (default: png)"
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
        "--expressions",
        nargs="+",
        choices=["excited", "smile", "serious", "surprised", "thoughtful"],
        help="Expressions to cycle through (default: all)"
    )

    args = parser.parse_args()

    # Try to load manifest
    manifest_path = f"src/{args.composition}/thumbnails/manifest.json"

    try:
        if os.path.exists(manifest_path):
            print(f"Loading manifest: {manifest_path}")
            spec = load_manifest(manifest_path)
        else:
            # Create spec from arguments
            if not args.concept:
                print(f"No manifest found at {manifest_path}", file=sys.stderr)
                print("Please provide --concept or create a manifest file", file=sys.stderr)
                return 1

            spec = ThumbnailSpec(
                concept=args.concept,
                composition=args.composition,
                style=args.style or DEFAULT_STYLE,
            )

        # Override with command line arguments
        if args.style:
            spec.style = args.style
        if args.concept:
            spec.concept = args.concept
        if args.model:
            spec.model = args.model

        # Determine output directory
        output_dir = args.output_dir or f"public/thumbnails/{args.composition.lower()}"

        # Check if using face reference
        use_face_ref = args.face_ref or args.face_url

        # Generate variations
        print("\n" + "=" * 60)
        print("YouTube Thumbnail Variation Generator")
        print("=" * 60)
        print(f"\nComposition: {args.composition}")
        print(f"Style: {spec.style}")
        print(f"Output: {output_dir}")
        print(f"Variations: {args.count}")

        if use_face_ref:
            print(f"Face model: {args.face_model}")
            print(f"Face weight: {args.face_weight}")
            if args.expressions:
                print(f"Expressions: {', '.join(args.expressions)}")

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
            )

            print()

            results = generate_face_variations(
                spec=face_spec,
                output_dir=output_dir,
                count=args.count,
                output_format=args.format,
                expressions=args.expressions,
            )
        else:
            print()

            results = generate_variations(
                spec=spec,
                output_dir=output_dir,
                count=args.count,
                output_format=args.format,
            )

        # Print summary
        success_count = sum(1 for r in results if r.get("success"))
        total_cost = sum(r.get("cost", 0) for r in results if r.get("success"))

        print("\n" + "=" * 60)
        print("Summary")
        print("=" * 60)
        print(f"\nSuccessful: {success_count}/{args.count}")
        print(f"Total cost: ${total_cost:.3f}")
        print(f"\nOutput directory: {output_dir}")
        print("\nNext steps:")
        print("  1. Review generated thumbnails")
        print("  2. Add text overlays (Canva/Photoshop)")
        print("  3. Run mobile test (150px width)")
        print("  4. Select 2-3 for A/B testing")

        return 0 if success_count > 0 else 1

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
