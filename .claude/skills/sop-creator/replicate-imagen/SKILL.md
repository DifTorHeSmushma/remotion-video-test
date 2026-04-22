---
name: replicate-imagen
description: Generate AI images using Replicate's google/imagen-4-fast model for video scenes. Use when creating visual assets for Remotion compositions, generating scene backgrounds, hero images, or illustrative graphics. Handles aspect ratios for both landscape (16:9) and vertical (9:16) videos.
---

# Replicate Imagen Image Generator

Generate high-quality AI images for video scenes using Google's Imagen 4 Fast model via Replicate API.

## Quick Start

### Single Image Generation
```bash
python generate-image.py \
  --prompt "A futuristic terminal interface with glowing cyan code" \
  --output-dir public/images/my-video/ \
  --name scene01-hero \
  --aspect-ratio 16:9
```

### Batch Generation from Manifest
```bash
python generate-scene-images.py MyVideoName
```

## Configuration

Add to `.env`:
```bash
REPLICATE_API_TOKEN=your-token-here
REPLICATE_DEFAULT_ASPECT_RATIO=16:9
REPLICATE_DEFAULT_OUTPUT_FORMAT=png
```

Get your API token from: https://replicate.com/account/api-tokens

## Model Details

**Model**: `google/imagen-4-fast`
**Cost**: $0.02 per image (50 images for $1)
**Speed**: Fast generation (~5-10 seconds)

### Supported Aspect Ratios
| Ratio | Use Case |
|-------|----------|
| `16:9` | Standard video scenes (1920x1080) |
| `9:16` | YouTube Shorts (1080x1920) |
| `1:1` | Square images, icons |
| `4:3` | Traditional video |
| `3:4` | Portrait images |

### Output Formats
- `png` (default) - Best for graphics with transparency needs
- `jpg` - Smaller files, good for photos

## Manifest Format

Create `src/<AnimationName>/images/manifest.json`:

```json
{
  "composition": "MyVideoName",
  "description": "Images for the MyVideoName explainer video",
  "images": [
    {
      "name": "scene01-hero",
      "prompt": "A photorealistic futuristic workspace with multiple holographic screens displaying code. Dark environment with cyan and purple accent lighting. Ultra-detailed, cinematic composition.",
      "aspect_ratio": "16:9",
      "usage": "Hero image for hook scene"
    },
    {
      "name": "scene03-diagram",
      "prompt": "Clean technical diagram showing data flow between connected nodes. Minimalist design with dark background and glowing blue connection lines. Flat design style.",
      "aspect_ratio": "16:9",
      "usage": "Architecture diagram background"
    }
  ]
}
```

## Prompt Engineering Tips

### For Video Scenes

1. **Be Specific**: Include lighting, style, and composition details
2. **Match Video Tone**: Use consistent visual language across prompts
3. **Consider Motion**: Images may have animated elements overlaid
4. **Dark Backgrounds**: Work best with text overlays and motion graphics

### Prompt Template for Tech Videos
```
[Subject description]. [Style/mood]. [Lighting]. [Technical details].
Dark environment with [primary color] and [accent color] lighting.
Ultra-detailed, cinematic composition, 8K quality.
```

### Example Prompts by Scene Type

**Hook Scene (attention-grabbing)**:
```
A dramatic explosion of digital particles forming a neural network pattern.
Electric blue and purple energy streams against deep black void.
Hyper-detailed, cinematic lighting, volumetric effects.
```

**Technical Diagram**:
```
Clean isometric view of a container architecture with labeled components.
Minimalist design on dark gradient background.
Glowing cyan connection lines, subtle grid pattern.
Professional technical illustration style.
```

**Feature Showcase**:
```
Split-screen comparison of old vs new code editor interfaces.
Left side dark and cluttered, right side sleek and modern.
Soft ambient lighting highlighting the contrast.
```

**CTA Scene**:
```
A glowing "Subscribe" button floating in space with particle effects.
Warm orange and gold tones radiating outward.
Clean, inviting, friendly atmosphere.
```

## Integration with Video Workflow

### Phase 1 (Planning)
Add image specifications to the plan file:
```yaml
images:
  - scene: hook
    name: scene01-hero
    prompt: "..."
    aspect_ratio: "16:9"
```

### Phase 4 (Sync)
1. Create manifest from plan specifications
2. Run batch generation:
   ```bash
   python generate-scene-images.py <AnimationName>
   ```
3. Use in scenes:
   ```tsx
   import { Img, staticFile } from 'remotion';

   <Img src={staticFile('images/myvideoname/scene01-hero.png')} />
   ```

## Using Generated Images in Remotion

### Basic Image Display
```tsx
import { Img, staticFile, interpolate, useCurrentFrame } from 'remotion';

export const Scene01Hook: React.FC = () => {
  const frame = useCurrentFrame();

  // Animate opacity
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill>
      <Img
        src={staticFile('images/myvideoname/scene01-hero.png')}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          opacity,
        }}
      />
    </AbsoluteFill>
  );
};
```

### Ken Burns Effect (Slow Zoom)
```tsx
const scale = interpolate(frame, [0, 300], [1, 1.1], {
  extrapolateRight: 'clamp',
});

<Img
  src={staticFile('images/myvideoname/scene01-hero.png')}
  style={{
    transform: `scale(${scale})`,
    transformOrigin: 'center center',
  }}
/>
```

### Background with Overlay
```tsx
<AbsoluteFill>
  {/* Background image */}
  <Img
    src={staticFile('images/myvideoname/scene-bg.png')}
    style={{ width: '100%', height: '100%', objectFit: 'cover' }}
  />

  {/* Dark overlay for text readability */}
  <div style={{
    position: 'absolute',
    inset: 0,
    background: 'linear-gradient(to bottom, rgba(0,0,0,0.3), rgba(0,0,0,0.7))',
  }} />

  {/* Content on top */}
  <TextContent />
</AbsoluteFill>
```

## Troubleshooting

### "Missing REPLICATE_API_TOKEN"
Ensure `.env` contains your token:
```bash
REPLICATE_API_TOKEN=r8_your_actual_token_here
```

### Image URL Expired
Replicate image URLs expire after 24 hours. The library automatically downloads images immediately after generation.

### Safety Filter Blocking
If images are blocked, the prompt may contain restricted content. Try:
- Making the prompt more abstract
- Removing references to people or brands
- Using technical/diagram style instead of photorealistic

### Wrong Aspect Ratio
Verify you're using the correct ratio for your video:
- `16:9` for standard 1920x1080 videos
- `9:16` for YouTube Shorts (1080x1920)

## Cost Estimation

| Video Type | Scenes | Images/Scene | Total Images | Cost |
|------------|--------|--------------|--------------|------|
| 60s explainer | 7 | 1-2 | 7-14 | $0.14-$0.28 |
| 5min tutorial | 12 | 2-3 | 24-36 | $0.48-$0.72 |
| YouTube Short | 3 | 1 | 3 | $0.06 |

## Quick Reference

```bash
# Single image
python generate-image.py -p "prompt" -o public/images/name/ -n image-name

# Batch from manifest
python generate-scene-images.py AnimationName

# Check token is set
echo $REPLICATE_API_TOKEN
```
