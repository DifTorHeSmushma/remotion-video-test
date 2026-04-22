# Model Selection Guide

## Decision Matrix

| Use Case | Best Model | Why | Key Settings |
|----------|-----------|-----|--------------|
| **Audiobooks/Narration** | Multilingual v2 | Stability, quality, 10k char limit | Stability: 55-70 |
| **Real-time Agents** | Flash v2.5 | 75ms latency, streaming support | Manual normalization required |
| **Dramatic Performance** | Eleven v3 | Emotional range, audio tags | Generate 3-5 versions |
| **Technical Documentation** | Multilingual v2 | Auto number normalization | Stability: 60-75 |
| **Conversational AI** | Flash v2.5 or Turbo v2.5 | Low latency, WebSocket support | Streaming enabled |
| **Multi-character Dialogue** | Eleven v3 | Single voice, multiple characters | Use Text-to-Dialogue API |
| **Corporate/Professional** | Multilingual v2 | Consistency, reliability | Stability: 60-75 |
| **Creative Content** | Eleven v3 | Expressiveness, effects | Audio tags, >250 chars |
| **Bulk Processing** | Flash v2.5 | Cost-effective (50% less) | Batch processing |
| **International Content** | Multilingual v2 or v3 | v2: 29 languages, v3: 70+ | Match voice to language |

## Model Capabilities

### Eleven v3 (Alpha)
**Strengths:**
- Revolutionary expressiveness
- Audio tags for emotion/delivery
- Multi-character with one voice
- 70+ languages
- Human reactions (laughs, sighs)

**Limitations:**
- 3,000 character limit
- Non-deterministic (requires multiple generations)
- Not for real-time (no streaming)
- Professional Voice Clones not optimized
- Alpha status (may change)

**When to Use:**
- Dramatic narration
- Character dialogue
- Emotional content
- Creative projects
- When expressiveness > consistency

### Multilingual v2
**Strengths:**
- Best overall quality
- Automatic number normalization
- 10,000 character limit
- Stable and predictable
- 29 languages
- Professional Voice Clone support

**Limitations:**
- Higher latency than v2.5 models
- No phoneme tags
- Traditional dialogue format only

**When to Use:**
- Professional narration
- Audiobooks
- Long-form content
- Technical documentation
- When quality > speed

### Flash v2.5
**Strengths:**
- Ultra-low latency (75ms)
- 40,000 character limit
- Phoneme tag support
- 50% lower cost
- 32 languages
- WebSocket streaming

**Limitations:**
- No automatic number normalization
- Lower quality than v2
- Requires preprocessing

**When to Use:**
- Real-time applications
- Conversational agents
- High-volume processing
- When speed > quality

### Turbo v2.5
**Strengths:**
- Balanced speed/quality
- 250-300ms latency
- Number normalization enabled
- 40,000 character limit
- 32 languages

**Limitations:**
- No phoneme tags (unlike Flash)
- Not as fast as Flash
- Not as good as Multilingual v2

**When to Use:**
- General purpose TTS
- When Flash is too low quality
- When v2 is too slow

## Feature Compatibility

| Feature | v3 | Multilingual v2 | Flash v2.5 | Turbo v2.5 |
|---------|-------|-----------------|------------|------------|
| Audio tags | ✅ | ❌ | ❌ | ❌ |
| Phoneme tags | ❌ | ❌ | ✅ | ❌ |
| Break tags | ❌ | ✅ | ✅ | ✅ |
| Auto normalization | ✅ | ✅ | ❌* | ✅ |
| Streaming | ❌ | ✅ | ✅ | ✅ |
| WebSocket | ❌ | ❌ | ✅ | ✅ |
| Prof. Voice Clone | ❌** | ✅ | ✅ | ✅ |
| Text-to-Dialogue | ✅ | ❌ | ❌ | ❌ |

*Can be enabled for Enterprise
**Coming in future update

## Latency Comparison

```
Flash v2.5:        ~75ms    ████
Turbo v2.5:        ~250ms   ████████████
Multilingual v2:   ~400ms   ████████████████████
Eleven v3:         Variable ████████████████████████████
```

## Cost Comparison (Relative)

```
Flash v2.5:        50% cost  ████████████
Turbo v2.5:        100% cost ████████████████████████
Multilingual v2:   100% cost ████████████████████████
Eleven v3:         100% cost ████████████████████████
```

## Model Selection Flowchart

```
Start → Need real-time? 
         ├─ Yes → Need quality?
         │         ├─ Yes → Turbo v2.5
         │         └─ No → Flash v2.5
         └─ No → Need expressiveness?
                   ├─ Yes → v3 (if <3k chars)
                   └─ No → Need quality?
                           ├─ Yes → Multilingual v2
                           └─ No → Flash v2.5 (cost savings)
```

## Quick Decision Rules

1. **Default choice**: Multilingual v2
2. **For speed**: Flash v2.5
3. **For expression**: Eleven v3
4. **For balance**: Turbo v2.5
5. **For cost**: Flash v2.5
6. **For quality**: Multilingual v2
7. **For dialogue**: Eleven v3
8. **For real-time**: Flash v2.5
9. **For audiobooks**: Multilingual v2
10. **For emotions**: Eleven v3
