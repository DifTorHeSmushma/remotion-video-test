"""
Core YouTube thumbnail generation library using Replicate AI models.
Supports google/imagen-4-fast for photorealistic backgrounds and
black-forest-labs/flux for text-heavy designs.

Face reference support via InstantID, FLUX PuLID, and IP-Adapter models.

Shared by generate-thumbnail.py (single) and generate-thumbnail-variations.py (batch).
"""

import os
import json
import requests
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
import replicate
from PIL import Image

load_dotenv()

REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Thumbnail settings from .env (with defaults)
DEFAULT_MODEL = os.getenv("THUMBNAIL_DEFAULT_MODEL", "nano-banana")
DEFAULT_STYLE = os.getenv("THUMBNAIL_DEFAULT_STYLE", "tech-dramatic")
DEFAULT_OUTPUT_FORMAT = os.getenv("REPLICATE_DEFAULT_OUTPUT_FORMAT", "png")

# YouTube thumbnail specifications
YOUTUBE_WIDTH = 1920
YOUTUBE_HEIGHT = 1080
YOUTUBE_ASPECT_RATIO = "16:9"
YOUTUBE_MAX_FILE_SIZE_MB = 2

# Model configurations with costs and capabilities
MODELS: Dict[str, Dict[str, Any]] = {
    "imagen": {
        "name": "google/imagen-4-fast",
        "version": "1589f5c0d4c45e72e9b7fd0914f0a985476bbfb54a6d1ddf5b7579ac830b15e3",
        "cost_per_image": 0.02,
        "text_rendering": "poor",
        "best_for": "Photorealistic backgrounds, scenes without text",
        "supports_aspect_ratio": True,
    },
    "nano-banana": {
        "name": "google/nano-banana-pro",
        "version": None,  # Uses latest
        "cost_per_image": 0.04,
        "text_rendering": "good",
        "best_for": "High quality photorealistic thumbnails with image reference support",
        "supports_aspect_ratio": True,
    },
    "flux-pro": {
        "name": "black-forest-labs/flux-1.1-pro",
        "version": None,  # Uses latest
        "cost_per_image": 0.04,
        "text_rendering": "excellent",
        "best_for": "Text-heavy designs, typography, logos",
        "supports_aspect_ratio": True,
    },
    "flux-schnell": {
        "name": "black-forest-labs/flux-schnell",
        "version": None,  # Uses latest
        "cost_per_image": 0.003,
        "text_rendering": "good",
        "best_for": "Quick iterations, drafts, testing",
        "supports_aspect_ratio": True,
    },
    "flux-thumbnails": {
        "name": "justmalhar/flux-thumbnails-v3",
        "version": "f0db143a6467cfb2b6b1408b6454d120061f35102b1f660af23ce4d91f7940db",
        "cost_per_image": 0.02,
        "text_rendering": "excellent",
        "best_for": "YouTube thumbnails with text overlays, fine-tuned for CTR",
        "supports_aspect_ratio": True,
        "prompt_prefix": "a youtube thumbnail in the style of YTTHUMBNAIL, ",
    },
    "diysmartcode": {
        "name": "leex279/diysmartcode-thumbnails",
        "version": "998ed156c1d2669aeddb05b2b3d12405b81007facddacaa389cfbd5bf60b8505",
        "cost_per_image": 0.02,
        "text_rendering": "good",
        "best_for": "DIYSmartCode brand thumbnails with consistent style",
        "supports_aspect_ratio": True,
    },
}

# Face reference models for identity preservation
FACE_REF_MODELS: Dict[str, Dict[str, Any]] = {
    "diysmartcode": {
        "name": "leex279/diysmartcode-thumbnails",
        "version": "998ed156c1d2669aeddb05b2b3d12405b81007facddacaa389cfbd5bf60b8505",
        "cost_per_image": 0.02,
        "face_consistency": "95%+",
        "best_for": "Custom fine-tuned model for DIYSmartCode thumbnails (recommended)",
        "supports_multiple_refs": False,
    },
    "nano-banana": {
        "name": "google/nano-banana-pro",
        "cost_per_image": 0.04,
        "face_consistency": "95%+",
        "best_for": "Gemini 2.5 Pro - best consistency, surpasses FLUX Kontext",
        "supports_multiple_refs": False,
    },
    "flux-kontext": {
        "name": "black-forest-labs/flux-kontext-pro",
        "cost_per_image": 0.04,
        "face_consistency": "90%+",
        "best_for": "High-quality face preservation with FLUX",
        "supports_multiple_refs": False,
    },
    "instant-id": {
        "name": "zsxkib/instant-id",
        "cost_per_image": 0.02,
        "face_consistency": "85%+",
        "best_for": "Zero-shot identity preservation",
        "supports_multiple_refs": False,
    },
    "instant-id-photo": {
        "name": "grandlineai/instant-id-photorealistic",
        "cost_per_image": 0.02,
        "face_consistency": "85%+",
        "best_for": "Photorealistic identity preservation",
        "supports_multiple_refs": False,
    },
}

# Default face reference model
DEFAULT_FACE_MODEL = os.getenv("THUMBNAIL_FACE_MODEL", "flux-kontext")
DEFAULT_FACE_WEIGHT = float(os.getenv("THUMBNAIL_FACE_WEIGHT", "0.8"))

# Style presets with prompt suffixes
STYLE_PRESETS: Dict[str, Dict[str, str]] = {
    "tech-dramatic": {
        "description": "Dark background with neon accents and dramatic lighting",
        "suffix": "Dark gradient background transitioning from deep navy to black. Dramatic rim lighting with neon cyan and purple accents. Professional tech aesthetic. Ultra-sharp details. Clean composition with clear focal point.",
        "best_for": "Coding, AI, tech tutorials",
        "recommended_model": "imagen",
    },
    "before-after": {
        "description": "Split composition showing transformation",
        "suffix": "Split composition with clear visual divide. Left side shows 'before' state (muted, grayscale tones). Right side shows 'after' state (vibrant, colorful). Clear contrast and visual storytelling. Professional transformation thumbnail style.",
        "best_for": "Tutorials, transformations, comparisons",
        "recommended_model": "imagen",
    },
    "stats-impact": {
        "description": "Large numbers with minimal design",
        "suffix": "Clean minimal design with large prominent numbers as focal point. Subtle gradient background. High contrast for readability. Professional data visualization aesthetic. Clear visual hierarchy.",
        "best_for": "Data videos, statistics, benchmarks",
        "recommended_model": "flux-pro",
    },
    "face-reaction": {
        "description": "Expressive face with bold text overlay zone",
        "suffix": "Dramatic portrait lighting with expressive facial features. Clear space on right third for text overlay. High contrast and saturation. YouTube thumbnail composition with emotional impact.",
        "best_for": "Reviews, commentary, reactions",
        "recommended_model": "imagen",
    },
    "minimalist": {
        "description": "Clean single element design",
        "suffix": "Clean minimalist design with single focal element. Subtle gradient or solid color background. Generous white space. Professional and elegant. High-end aesthetic with clear visual focus.",
        "best_for": "Professional, educational content",
        "recommended_model": "imagen",
    },
    "curiosity-gap": {
        "description": "Partial reveal creating mystery",
        "suffix": "Mysterious composition with partial reveal. Strategic use of shadows and blur to obscure details. Creates visual curiosity and intrigue. Dramatic lighting with dark tones. Compelling mystery aesthetic.",
        "best_for": "Teasers, reveals, storytelling",
        "recommended_model": "imagen",
    },
    "high-energy": {
        "description": "Vibrant colors with dynamic composition",
        "suffix": "High energy vibrant colors with dynamic diagonal composition. Explosive visual elements. Bold saturated hues. Action-oriented aesthetic. Eye-catching and attention-grabbing.",
        "best_for": "Entertainment, gaming, fast-paced content",
        "recommended_model": "imagen",
    },
    "professional": {
        "description": "Corporate clean design",
        "suffix": "Professional corporate aesthetic. Clean lines and balanced composition. Muted color palette with subtle accent color. Business-appropriate with clear visual hierarchy. Trust-building design.",
        "best_for": "Business, enterprise, formal content",
        "recommended_model": "imagen",
    },
}


@dataclass
class ThumbnailSpec:
    """Specification for a YouTube thumbnail."""

    concept: str  # Main visual concept/scene
    title: Optional[str] = None  # Video title for context
    composition: Optional[str] = None  # Composition name for organization
    style: str = "tech-dramatic"  # Style preset ID
    text_overlay: Optional[Dict[str, Any]] = None  # Text overlay config
    brand_colors: Optional[Dict[str, str]] = None  # Brand color palette
    model: Optional[str] = None  # Override model selection

    def __post_init__(self):
        if self.style not in STYLE_PRESETS:
            raise ValueError(f"Unknown style: {self.style}. Available: {list(STYLE_PRESETS.keys())}")


@dataclass
class ThumbnailWithFaceSpec(ThumbnailSpec):
    """Extended specification for face-aware thumbnail generation."""

    face_ref_dir: Optional[str] = None  # Directory with reference images
    face_ref_url: Optional[str] = None  # Direct URL to face image
    face_model: str = "instant-id-plus"  # Face reference model
    face_weight: float = 0.8  # Face preservation strength (0.01-2)
    expression: Optional[str] = None  # Desired expression (excited, smile, serious)

    def __post_init__(self):
        super().__post_init__()
        if self.face_model not in FACE_REF_MODELS:
            raise ValueError(f"Unknown face model: {self.face_model}. Available: {list(FACE_REF_MODELS.keys())}")


def select_model(style: str, has_text: bool = False) -> str:
    """
    Select the best model based on style and text requirements.

    Args:
        style: Style preset ID
        has_text: Whether the thumbnail will have text rendered by AI

    Returns:
        Model ID (imagen, flux-pro, or flux-schnell)
    """
    # If text needs to be rendered by AI (not overlay), use FLUX
    if has_text:
        return "flux-pro"

    # Otherwise, use style's recommended model
    preset = STYLE_PRESETS.get(style, STYLE_PRESETS["tech-dramatic"])
    return preset.get("recommended_model", "imagen")


def build_thumbnail_prompt(spec: ThumbnailSpec) -> str:
    """
    Build a complete prompt from a ThumbnailSpec.

    Args:
        spec: ThumbnailSpec with concept and style

    Returns:
        Complete prompt string for image generation
    """
    parts = []

    # Main concept
    parts.append(spec.concept.strip())

    # Add "Professional YouTube thumbnail style" marker
    parts.append("Professional YouTube thumbnail style.")

    # Style-specific suffix
    preset = STYLE_PRESETS.get(spec.style, STYLE_PRESETS["tech-dramatic"])
    parts.append(preset["suffix"])

    # Text overlay zone if specified
    if spec.text_overlay and spec.text_overlay.get("enabled"):
        position = spec.text_overlay.get("position", "right")
        if position == "right":
            parts.append("Clear space on right third for text overlay.")
        elif position == "left":
            parts.append("Clear space on left third for text overlay.")
        elif position == "bottom":
            parts.append("Clear space on bottom third for text overlay.")
        elif position == "top":
            parts.append("Clear space on top third for text overlay.")

    # Brand color hints if provided
    if spec.brand_colors:
        primary = spec.brand_colors.get("primary")
        accent = spec.brand_colors.get("accent")
        if primary or accent:
            color_hint = "Color scheme featuring"
            if primary:
                color_hint += f" {primary} as primary"
            if accent:
                color_hint += f" and {accent} as accent"
            color_hint += " color."
            parts.append(color_hint)

    # Technical requirements
    parts.append("16:9 aspect ratio, 1920x1080 full HD resolution, ultra-sharp, high quality.")

    return " ".join(parts)


def _download_and_save(output, output_path: str) -> bool:
    """
    Download image from Replicate output and save to disk.

    Args:
        output: Replicate API output (FileOutput, URL, or list)
        output_path: Path to save the image

    Returns:
        True if successful
    """
    # Handle FileOutput object with read() method
    if hasattr(output, 'read'):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(output.read())
        return True

    # Handle URL attribute
    if hasattr(output, 'url'):
        image_url = output.url
    elif isinstance(output, list):
        first_item = output[0]
        if hasattr(first_item, 'read'):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(first_item.read())
            return True
        elif hasattr(first_item, 'url'):
            image_url = first_item.url
        else:
            image_url = str(first_item)
    else:
        image_url = str(output)

    # Download from URL
    response = requests.get(image_url)
    response.raise_for_status()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)

    return True


def generate_thumbnail(
    spec: ThumbnailSpec,
    output_path: str,
    output_format: str = None,
) -> Dict[str, Any]:
    """
    Generate a YouTube thumbnail using Replicate.

    Args:
        spec: ThumbnailSpec with concept and configuration
        output_path: Full path for the output image file
        output_format: "jpg" or "png" (default from env)

    Returns:
        dict with keys: success, path, prompt, model, style, cost

    Raises:
        ValueError: If REPLICATE_API_TOKEN is missing
        Exception: If API call or download fails
    """
    if not REPLICATE_API_TOKEN:
        raise ValueError("Missing REPLICATE_API_TOKEN in .env file!")

    output_format = output_format or DEFAULT_OUTPUT_FORMAT

    # Select model
    has_text = spec.text_overlay and spec.text_overlay.get("ai_render_text", False)
    model_id = spec.model or select_model(spec.style, has_text)
    model_config = MODELS.get(model_id, MODELS["imagen"])

    # Build prompt
    prompt = build_thumbnail_prompt(spec)

    # Apply model-specific prompt prefix (e.g., YTTHUMBNAIL style token)
    prompt_prefix = model_config.get("prompt_prefix", "")
    if prompt_prefix:
        prompt = prompt_prefix + prompt

    print(f"  Generating thumbnail: {os.path.basename(output_path)}")
    print(f"  Model: {model_config['name']}")
    print(f"  Style: {spec.style}")
    print(f"  Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}")

    # Prepare API input
    api_input = {
        "prompt": prompt,
        "aspect_ratio": YOUTUBE_ASPECT_RATIO,
    }

    # Add model-specific parameters
    if model_id == "imagen":
        api_input["output_format"] = output_format
        api_input["safety_filter_level"] = "block_only_high"
    elif model_id == "flux-thumbnails":
        api_input["guidance_scale"] = 3.5
        api_input["output_quality"] = 90
    elif model_id == "nano-banana":
        api_input["resolution"] = "1K"
        api_input["image_input"] = []
        api_input["output_format"] = output_format
        api_input["safety_filter_level"] = "block_only_high"
        api_input["allow_fallback_model"] = False
        print(f"  Params: resolution=1K, image_input=[], safety_filter_level=block_only_high, allow_fallback_model=False")

    # Call Replicate API
    # Use version-specific identifier if provided
    model_identifier = model_config["name"]
    if model_config.get("version"):
        model_identifier = f"{model_config['name']}:{model_config['version']}"

    output = replicate.run(
        model_identifier,
        input=api_input
    )

    # Download and save
    _download_and_save(output, output_path)

    file_size = os.path.getsize(output_path)
    file_size_mb = file_size / (1024 * 1024)
    print(f"  Saved: {output_path} ({file_size / 1024:.1f} KB)")

    # Warn if file exceeds YouTube limit
    if file_size_mb > YOUTUBE_MAX_FILE_SIZE_MB:
        print(f"  WARNING: File size ({file_size_mb:.2f} MB) exceeds YouTube limit ({YOUTUBE_MAX_FILE_SIZE_MB} MB)")

    return {
        "success": True,
        "path": output_path,
        "prompt": prompt,
        "model": model_config["name"],
        "model_id": model_id,
        "style": spec.style,
        "cost": model_config["cost_per_image"],
        "file_size_kb": file_size / 1024,
    }


def generate_variations(
    spec: ThumbnailSpec,
    output_dir: str,
    count: int = 5,
    output_format: str = None,
) -> List[Dict[str, Any]]:
    """
    Generate multiple thumbnail variations for A/B testing.

    Args:
        spec: ThumbnailSpec with concept and configuration
        output_dir: Directory for output images
        count: Number of variations to generate (default 5)
        output_format: "jpg" or "png" (default from env)

    Returns:
        List of result dicts from generate_thumbnail()
    """
    results = []
    output_format = output_format or DEFAULT_OUTPUT_FORMAT

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate base name from composition or concept
    base_name = spec.composition or "thumbnail"
    base_name = base_name.lower().replace(" ", "-")

    print(f"Generating {count} thumbnail variations...")
    print(f"Output directory: {output_dir}\n")

    total_cost = 0

    for i in range(1, count + 1):
        output_path = os.path.join(output_dir, f"{base_name}-v{i:02d}.{output_format}")

        print(f"--- Variation {i}/{count} ---")

        try:
            result = generate_thumbnail(
                spec=spec,
                output_path=output_path,
                output_format=output_format,
            )
            results.append(result)
            total_cost += result.get("cost", 0)
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                "success": False,
                "variation": i,
                "error": str(e),
            })

        print()

    # Summary
    success_count = sum(1 for r in results if r.get("success"))
    print(f"Generated {success_count}/{count} variations successfully")
    print(f"Total cost: ${total_cost:.3f}")

    return results


def load_manifest(manifest_path: str) -> ThumbnailSpec:
    """
    Load a ThumbnailSpec from a JSON manifest file.

    Manifest format:
    {
        "composition": "MyVideoName",
        "title": "How to 10x Your Coding Speed",
        "concept": "AI coding assistant productivity",
        "style_primary": "tech-dramatic",
        "text_overlay": {
            "enabled": true,
            "words": ["10x", "Faster"],
            "position": "right"
        },
        "brand_colors": {
            "primary": "#a855f7",
            "accent": "#06b6d4"
        }
    }

    Args:
        manifest_path: Path to JSON manifest file

    Returns:
        ThumbnailSpec instance
    """
    with open(manifest_path, "r") as f:
        manifest = json.load(f)

    return ThumbnailSpec(
        concept=manifest.get("concept", ""),
        title=manifest.get("title"),
        composition=manifest.get("composition"),
        style=manifest.get("style_primary", manifest.get("style", DEFAULT_STYLE)),
        text_overlay=manifest.get("text_overlay"),
        brand_colors=manifest.get("brand_colors"),
        model=manifest.get("model"),
    )


def get_style_info(style_id: str = None) -> Dict[str, Any]:
    """
    Get information about style presets.

    Args:
        style_id: Specific style to get info for, or None for all

    Returns:
        Style info dict or dict of all styles
    """
    if style_id:
        if style_id not in STYLE_PRESETS:
            raise ValueError(f"Unknown style: {style_id}")
        return {style_id: STYLE_PRESETS[style_id]}
    return STYLE_PRESETS


def get_model_info(model_id: str = None) -> Dict[str, Any]:
    """
    Get information about available models.

    Args:
        model_id: Specific model to get info for, or None for all

    Returns:
        Model info dict or dict of all models
    """
    if model_id:
        if model_id not in MODELS:
            raise ValueError(f"Unknown model: {model_id}")
        return {model_id: MODELS[model_id]}
    return MODELS


def get_face_model_info(model_id: str = None) -> Dict[str, Any]:
    """
    Get information about available face reference models.

    Args:
        model_id: Specific model to get info for, or None for all

    Returns:
        Face model info dict or dict of all face models
    """
    if model_id:
        if model_id not in FACE_REF_MODELS:
            raise ValueError(f"Unknown face model: {model_id}")
        return {model_id: FACE_REF_MODELS[model_id]}
    return FACE_REF_MODELS


def select_best_face_reference(directory: str) -> str:
    """
    Select the best quality face reference from a directory.
    Scores based on: image size, aspect ratio, filename hints.

    Args:
        directory: Path to directory containing face reference images

    Returns:
        Path to the best reference image
    """
    dir_path = Path(directory)
    image_files = list(dir_path.glob("*.jpg")) + list(dir_path.glob("*.png")) + list(dir_path.glob("*.jpeg"))

    if not image_files:
        raise ValueError(f"No images found in {directory}")

    best_image = None
    best_score = -1

    # Priority filenames (front-facing, neutral or excited expressions)
    priority_patterns = ["front-neutral", "front-excited", "front-smile", "01-front", "neutral", "front"]

    for img_path in image_files:
        try:
            img = Image.open(img_path)
            width, height = img.size

            # Base score from image size (larger is better, cap at 2M pixels)
            size_score = min(width * height, 2000000) / 2000000

            # Aspect ratio score (portrait-ish 0.7-1.3 is ideal for faces)
            aspect_ratio = height / width if width > 0 else 0
            aspect_score = 1.0 if 0.7 < aspect_ratio < 1.3 else 0.5

            # Filename priority boost
            filename_lower = img_path.stem.lower()
            priority_boost = 0
            for i, pattern in enumerate(priority_patterns):
                if pattern in filename_lower:
                    priority_boost = (len(priority_patterns) - i) * 0.1
                    break

            score = (size_score * 0.4) + (aspect_score * 0.3) + priority_boost

            if score > best_score:
                best_score = score
                best_image = img_path

            img.close()
        except Exception:
            continue

    if not best_image:
        raise ValueError(f"Could not load any images from {directory}")

    return str(best_image)


def generate_thumbnail_with_face(
    spec: ThumbnailWithFaceSpec,
    output_path: str,
    output_format: str = None,
) -> Dict[str, Any]:
    """
    Generate YouTube thumbnail with consistent face reference.

    Args:
        spec: ThumbnailWithFaceSpec with face reference configuration
        output_path: Full path for output image
        output_format: "jpg" or "png" (default from env)

    Returns:
        dict with success, path, cost, model, face_model, etc.
    """
    if not REPLICATE_API_TOKEN:
        raise ValueError("Missing REPLICATE_API_TOKEN in .env file!")

    output_format = output_format or DEFAULT_OUTPUT_FORMAT

    # Get face reference image
    if spec.face_ref_dir:
        face_image_path = select_best_face_reference(spec.face_ref_dir)
        # Open as file for upload
        face_image = open(face_image_path, "rb")
        print(f"  Face reference: {os.path.basename(face_image_path)}")
    elif spec.face_ref_url:
        face_image = spec.face_ref_url
        print(f"  Face reference: {spec.face_ref_url[:50]}...")
    else:
        raise ValueError("Either face_ref_dir or face_ref_url is required")

    # Get face model config
    face_model_config = FACE_REF_MODELS.get(spec.face_model, FACE_REF_MODELS["flux-kontext"])

    # Build enhanced prompt
    prompt = build_thumbnail_prompt(spec)

    # Add expression hint if specified
    if spec.expression:
        expression_prompts = {
            "excited": "excited expression, wide eyes, raised eyebrows, energetic",
            "smile": "warm genuine smile, friendly, approachable",
            "serious": "serious focused expression, confident, professional",
            "surprised": "surprised expression, open mouth, shocked",
            "thoughtful": "thoughtful expression, contemplative, wise",
        }
        expr_hint = expression_prompts.get(spec.expression, spec.expression)
        prompt = f"{prompt} {expr_hint}."

    prompt += " Consistent face identity, professional headshot lighting."

    print(f"  Generating thumbnail with face reference: {os.path.basename(output_path)}")
    print(f"  Face model: {spec.face_model} ({face_model_config['name']})")
    print(f"  Face weight: {spec.face_weight}")
    print(f"  Expression: {spec.expression or 'default'}")

    # Model-specific API calls
    try:
        if spec.face_model == "diysmartcode":
            # Custom fine-tuned model for DIYSmartCode thumbnails
            api_input = {
                "prompt": prompt,
                "aspect_ratio": "16:9",
            }

        elif spec.face_model == "nano-banana":
            # Google Gemini 2.5 (Nano Banana) API parameters
            api_input = {
                "prompt": prompt,
                "resolution": "1K",
                "image_input": [face_image],
                "aspect_ratio": "16:9",
                "output_format": output_format,
                "safety_filter_level": "block_only_high",
                "allow_fallback_model": False,
            }
            print(f"  Params: resolution=1K, image_input=[<face_ref>], safety_filter_level=block_only_high, allow_fallback_model=False")

        elif spec.face_model == "flux-kontext":
            # FLUX Kontext Pro API parameters
            api_input = {
                "image": face_image,
                "prompt": prompt,
                "aspect_ratio": "16:9",
                "output_format": output_format,
                "safety_tolerance": 5,
            }

        elif spec.face_model == "instant-id":
            # zsxkib/instant-id API parameters
            api_input = {
                "image": face_image,
                "prompt": prompt,
                "negative_prompt": "lowres, bad anatomy, worst quality, low quality, blurry, distorted face",
                "num_inference_steps": 30,
                "guidance_scale": 5.0,
                "ip_adapter_scale": spec.face_weight,
                "controlnet_conditioning_scale": spec.face_weight,
                "width": YOUTUBE_WIDTH,
                "height": YOUTUBE_HEIGHT,
            }

        elif spec.face_model == "instant-id-photo":
            # grandlineai/instant-id-photorealistic API parameters
            api_input = {
                "image": face_image,
                "prompt": prompt,
                "negative_prompt": "lowres, bad anatomy, worst quality, low quality, blurry, distorted face",
                "num_inference_steps": 30,
                "guidance_scale": 5.0,
                "ip_adapter_scale": spec.face_weight,
                "controlnet_conditioning_scale": spec.face_weight,
            }

        else:
            raise ValueError(f"Unsupported face model: {spec.face_model}")

        # Call Replicate API - use version if provided
        model_identifier = face_model_config["name"]
        if face_model_config.get("version"):
            model_identifier = f"{face_model_config['name']}:{face_model_config['version']}"

        output = replicate.run(model_identifier, input=api_input)

        # Download and save
        _download_and_save(output, output_path)

        file_size = os.path.getsize(output_path)
        file_size_mb = file_size / (1024 * 1024)
        print(f"  Saved: {output_path} ({file_size / 1024:.1f} KB)")

        if file_size_mb > YOUTUBE_MAX_FILE_SIZE_MB:
            print(f"  WARNING: File size ({file_size_mb:.2f} MB) exceeds YouTube limit")

        return {
            "success": True,
            "path": output_path,
            "prompt": prompt,
            "model": face_model_config["name"],
            "face_model": spec.face_model,
            "style": spec.style,
            "face_weight": spec.face_weight,
            "expression": spec.expression,
            "cost": face_model_config["cost_per_image"],
            "file_size_kb": file_size / 1024,
        }

    finally:
        # Close file handle if we opened one
        if spec.face_ref_dir and hasattr(face_image, 'close'):
            face_image.close()


def generate_face_variations(
    spec: ThumbnailWithFaceSpec,
    output_dir: str,
    count: int = 5,
    output_format: str = None,
    expressions: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """
    Generate multiple thumbnail variations with consistent face for A/B testing.

    Args:
        spec: ThumbnailWithFaceSpec with face reference configuration
        output_dir: Directory for output images
        count: Number of variations to generate (default 5)
        output_format: "jpg" or "png" (default from env)
        expressions: List of expressions to cycle through

    Returns:
        List of result dicts from generate_thumbnail_with_face()
    """
    results = []
    output_format = output_format or DEFAULT_OUTPUT_FORMAT

    # Default expressions if not provided
    if not expressions:
        expressions = ["excited", "smile", "serious", "surprised", "thoughtful"]

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Generate base name
    base_name = spec.composition or "thumbnail"
    base_name = base_name.lower().replace(" ", "-")

    print(f"Generating {count} face thumbnail variations...")
    print(f"Face model: {spec.face_model}")
    print(f"Output directory: {output_dir}\n")

    total_cost = 0

    for i in range(1, count + 1):
        # Cycle through expressions
        expr = expressions[(i - 1) % len(expressions)]
        spec.expression = expr

        output_path = os.path.join(output_dir, f"{base_name}-face-v{i:02d}-{expr}.{output_format}")

        print(f"--- Variation {i}/{count} ({expr}) ---")

        try:
            result = generate_thumbnail_with_face(
                spec=spec,
                output_path=output_path,
                output_format=output_format,
            )
            results.append(result)
            total_cost += result.get("cost", 0)
        except Exception as e:
            print(f"  ERROR: {e}")
            results.append({
                "success": False,
                "variation": i,
                "expression": expr,
                "error": str(e),
            })

        print()

    # Summary
    success_count = sum(1 for r in results if r.get("success"))
    print(f"Generated {success_count}/{count} face variations successfully")
    print(f"Total cost: ${total_cost:.3f}")

    return results
