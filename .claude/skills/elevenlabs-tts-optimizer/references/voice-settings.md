# Voice Settings Optimization Guide

## Core Settings

### Stability (0-100)
Controls emotional variability and consistency of delivery.

**Low (0-30):** 
- Highly variable, expressive
- Risk of instability
- Use for: Extreme emotion, experimental

**Medium-Low (30-45):**
- Expressive, varied delivery
- Good for drama and storytelling
- Some risk of inconsistency

**Default (50):**
- Balanced expression and consistency
- Suitable for most content

**Medium-High (55-70):**
- Consistent delivery
- Professional narration quality
- Minimal variation

**High (70-100):**
- Very consistent, controlled
- Risk of monotone
- Use for: Technical content, consistency critical

### Similarity/Clarity (0-100)
Controls adherence to original voice characteristics.

**Low (0-50):**
- Less faithful to original
- May sound generic

**Optimal (70-80):**
- Best balance
- Clear, faithful reproduction
- Default: 75

**High (85-100):**
- Very faithful to training
- **WARNING**: May reproduce artifacts from training audio
- Only use with pristine training data

### Style Exaggeration (0-100)
Amplifies voice characteristics.

**Recommended: 0**
- Keep at 0 for most applications
- Increases latency
- Reduces stability
- Can cause mispronunciations

**When to Use (>0):**
- Specific artistic effect needed
- Short clips only
- Test thoroughly

### Speed (0.7-1.2)
Controls playback rate.

**Slow (0.7-0.8):**
- Educational content
- Accessibility needs
- Complex technical material

**Slightly Slow (0.8-0.9):**
- Audiobooks
- Thoughtful narration
- Elderly audiences

**Default (1.0):**
- General content
- Natural pacing

**Slightly Fast (1.1):**
- Energetic content
- Younger audiences
- Time-constrained material

**Fast (1.2):**
- Sports commentary
- Advertisements
- Risk of quality loss

## Content-Specific Presets

### Audiobook Narration
```
Model: Multilingual v2
Stability: 55-65
Similarity: 75-80
Style: 0
Speed: 0.9-1.0
```
*Consistent, clear, slightly slower for comprehension*

### Corporate/Professional
```
Model: Multilingual v2
Stability: 60-75
Similarity: 75-80
Style: 0
Speed: 1.0
```
*Reliable, professional, minimal variation*

### Storytelling/Drama
```
Model: v3 or Multilingual v2
Stability: 30-45
Similarity: 70-80
Style: 0
Speed: 0.9-1.0
```
*Expressive, varied, emotional range*

### Technical Documentation
```
Model: Multilingual v2
Stability: 65-75
Similarity: 75-80
Style: 0
Speed: 0.8-0.9
```
*Clear, consistent, slower for complex content*

### Real-time Conversation
```
Model: Flash v2.5
Stability: 50
Similarity: 75
Style: 0
Speed: 1.0
```
*Balanced for natural conversation*

### Educational Content
```
Model: Multilingual v2
Stability: 60-70
Similarity: 75-80
Style: 0
Speed: 0.8-0.9
```
*Clear, consistent, paced for learning*

### Marketing/Advertisement
```
Model: v3 or Multilingual v2
Stability: 40-50
Similarity: 75-80
Style: 0
Speed: 1.0-1.1
```
*Energetic, engaging, dynamic*

### Meditation/Relaxation
```
Model: Multilingual v2
Stability: 70-80
Similarity: 75-80
Style: 0
Speed: 0.7-0.8
```
*Calm, consistent, slow-paced*

## Voice Clone Optimization

### Instant Voice Clone Settings
```
Stability: 45-55
Similarity: 70-75
Style: 0
```
*Slightly lower similarity compensates for limited training*

### Professional Voice Clone Settings
```
Stability: 50-60
Similarity: 75-85
Style: 0
```
*Can use higher similarity due to better training*

## Troubleshooting Settings Issues

### Problem: Monotone Output
**Solution:** Decrease stability to 35-45

### Problem: Too Variable/Unstable
**Solution:** Increase stability to 60-70

### Problem: Doesn't Sound Like Voice
**Solution:** Increase similarity to 80-85 (if good training data)

### Problem: Reproducing Artifacts
**Solution:** Decrease similarity to 70-75

### Problem: Inconsistent Between Generations
**Solution:** Increase stability to 55-65

### Problem: Mispronunciations with Style
**Solution:** Set style exaggeration to 0

### Problem: Too Fast/Slow
**Solution:** Adjust speed in 0.1 increments

## Advanced Optimization

### Long-Form Content (>800 chars)
```
Stability: +10 from base setting
Similarity: 75 (consistent)
Style: 0 (always)
```
*Higher stability prevents drift*

### Multi-segment Generation
```
Use identical settings for all segments
Save settings as preset
Include in API parameters for consistency
```

### Voice Matching Across Sessions
```json
{
  "stability": 55,
  "similarity_boost": 75,
  "style": 0,
  "use_speaker_boost": false
}
```
*Document exact values for reproducibility*

## Settings by Voice Type

### Synthetic/AI Voices
```
Stability: 50-60
Similarity: 75
Style: 0
```

### Voice Design
```
Stability: 45-55
Similarity: 70-80
Style: 0
```

### Community Voices
```
Stability: 50-60
Similarity: 75-80
Style: 0
```

## API Parameter Examples

### Conservative/Safe
```python
settings = {
    "stability": 60,
    "similarity_boost": 75,
    "style": 0,
    "use_speaker_boost": False
}
```

### Expressive/Dynamic
```python
settings = {
    "stability": 35,
    "similarity_boost": 75,
    "style": 0,
    "use_speaker_boost": True
}
```

### Maximum Quality
```python
settings = {
    "stability": 55,
    "similarity_boost": 80,
    "style": 0,
    "use_speaker_boost": True,
    "model_id": "eleven_multilingual_v2"
}
```

## Quick Reference Table

| Goal | Stability | Similarity | Style | Speed |
|------|-----------|------------|-------|-------|
| Consistency | 60-75 | 75 | 0 | 1.0 |
| Expression | 30-45 | 75 | 0 | 1.0 |
| Natural | 50 | 75 | 0 | 1.0 |
| Professional | 65 | 80 | 0 | 1.0 |
| Dramatic | 35 | 75 | 0 | 0.9 |
| Technical | 70 | 75 | 0 | 0.8 |
| Fast-paced | 50 | 75 | 0 | 1.1 |
| Relaxed | 75 | 75 | 0 | 0.7 |

## Golden Rules

1. **Start with defaults** (50/75/0/1.0)
2. **Adjust one setting at a time**
3. **Style exaggeration stays at 0**
4. **Test with actual content**
5. **Document working settings**
6. **Higher stability for longer content**
7. **Match settings to voice training**
8. **Consistency > perfection for long-form**
9. **Generate multiple versions for v3**
10. **Save presets for repeatability**
