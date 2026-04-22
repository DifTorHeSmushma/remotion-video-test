# Troubleshooting Guide

## Common Issues and Solutions

### Pronunciation Problems

#### Issue: Numbers pronounced incorrectly
**Example:** "$1,000,000" spoken as "one thousand thousand dollars"

**Solutions:**
1. Write out numbers: `one million dollars`
2. Use Multilingual v2 (has auto normalization)
3. For Flash v2.5, always preprocess numbers
4. Use normalize_text.py script

#### Issue: Acronyms pronounced as words
**Example:** "SQL" pronounced as "sequel" instead of "S Q L"

**Solutions:**
1. Space letters: `S Q L`
2. Add pronunciation dictionary entry
3. Use phoneme tags (Flash v2.5 only)
4. Add dots: `S.Q.L.`

#### Issue: Names mispronounced
**Solutions:**
1. Phonetic respelling: `Nguyen` → `Win`
2. Phoneme tags: `<phoneme alphabet="cmu-arpabet" ph="W IH1 N">Nguyen</phoneme>`
3. Pronunciation dictionary with correct phonemes
4. Capital letters for emphasis: `ngWIN`

#### Issue: Foreign words with wrong accent
**Solutions:**
1. Use voice trained in that language
2. Phonetic respelling
3. Separate generation for foreign segments
4. Use v3 with accent tags: `[French accent] Bonjour`

### Audio Quality Issues

#### Issue: Voice becomes unstable/speeds up
**Cause:** Too many SSML break tags

**Solutions:**
1. Remove excessive break tags
2. Use natural punctuation instead
3. Maximum 3-4 break tags per generation
4. Space breaks throughout text

#### Issue: Background noise/artifacts
**Possible Causes:**
- Poor voice clone training data
- Similarity setting too high
- Corrupted generation

**Solutions:**
1. Reduce similarity to 70-75
2. Retrain voice clone with clean audio
3. Regenerate (v3 is non-deterministic)
4. Check training audio for artifacts

#### Issue: Voice switches accent mid-generation
**Cause:** Text over 800 characters

**Solutions:**
1. Split into <800 character segments
2. Use consistent voice settings
3. Add context parameters for continuity
4. Increase stability to 60+

#### Issue: Monotone delivery
**Solutions:**
1. Decrease stability to 35-45
2. Add punctuation for rhythm
3. Use v3 for more expression
4. Add emotional context (v2: dialogue tags)

### Model-Specific Issues

#### Issue: v3 audio tags spoken aloud
**Example:** Hearing "[laughs] That's funny"

**Solutions:**
1. Confirm using Eleven v3 model
2. Use Instant Clone or Voice Design (not Professional Clone yet)
3. Ensure prompt is >250 characters
4. Check model selection in API call

#### Issue: Flash v2.5 wrong number pronunciation
**Cause:** No automatic normalization

**Solutions:**
1. Always preprocess numbers to words
2. Use normalize_text.py script
3. Enable normalization (Enterprise only)
4. Switch to Turbo v2.5 or Multilingual v2

#### Issue: Phoneme tags not working
**Solutions:**
1. Only works with Flash v2, Turbo v2, English v1
2. Include stress markers for multi-syllable words
3. Check CMU Arpabet syntax
4. Verify model compatibility

### Generation Problems

#### Issue: Character limit exceeded
**Limits:**
- v3: 3,000 characters
- Multilingual v2: 10,000 characters  
- Flash/Turbo v2.5: 40,000 characters

**Solutions:**
1. Split text into appropriate segments
2. Use Studio for multi-segment management
3. Implement batching in code
4. Check character count before API call

#### Issue: Inconsistent results with v3
**Cause:** Non-deterministic model

**Solutions:**
1. Generate 3-5 versions
2. Select best output
3. Use consistent prompt structure
4. Ensure >250 character prompts

#### Issue: API rate limits hit
**Solutions:**
1. Monitor concurrent request headers
2. Implement exponential backoff
3. Check tier limits (Free: 2, Starter: 3, Creator: 5)
4. Upgrade subscription or add delays

### Voice Cloning Issues

#### Issue: Clone doesn't sound like original
**Solutions:**
1. Increase training data (30+ minutes for Professional)
2. Check audio quality (clean, consistent)
3. Match recording style to use case
4. Increase similarity setting to 80-85

#### Issue: Clone reproduces background noise
**Cause:** Training audio has noise

**Solutions:**
1. Clean training audio before cloning
2. Reduce similarity to 70-75
3. Re-record in treated environment
4. Use noise reduction (sparingly)

#### Issue: Clone has inconsistent quality
**Solutions:**
1. Use same microphone throughout recording
2. Maintain consistent distance/volume
3. Remove all filler words ("um", "ah")
4. Use single speaking style

### Formatting Problems

#### Issue: Pauses too long/short
**Solutions:**
1. Adjust break tag duration (max 3s)
2. Use punctuation for natural pauses
3. Try ellipses for hesitation
4. Use v3 pause tags: `[pause]`, `[long pause]`

#### Issue: Lists sound robotic
**Solutions:**
1. Use narrative format: "First, do this. Second, do that."
2. Add transition phrases
3. Include natural punctuation
4. Break into paragraphs

#### Issue: Dialogue tags spoken in v2
**Example:** Hearing "she said angrily"

**Solutions:**
1. Switch to v3 with audio tags
2. Remove in post-production
3. Use separate voices per character
4. Accept as limitation of v2

### Performance Issues

#### Issue: High latency for real-time
**Solutions:**
1. Use Flash v2.5 (75ms)
2. Enable streaming/WebSocket
3. Set optimize_streaming_latency parameter
4. Use geographic distribution (preview)

#### Issue: Credits consumed quickly
**Solutions:**
1. Cache generated audio
2. Use Flash v2.5 (50% cost)
3. Avoid regenerating same content
4. Monitor usage via API

## Quick Diagnostic Flowchart

```
Audio Problem?
├─ Quality Issue?
│  ├─ Noise/Artifacts → Check training data & similarity
│  ├─ Unstable → Reduce break tags, increase stability
│  └─ Monotone → Decrease stability, add punctuation
├─ Pronunciation Issue?
│  ├─ Numbers → Normalize text or use Multilingual v2
│  ├─ Names → Phoneme tags or dictionary
│  └─ Acronyms → Space letters or alias
└─ Generation Issue?
   ├─ Inconsistent → Use v2 or generate multiple v3
   ├─ Wrong model features → Check model compatibility
   └─ Rate limited → Check tier & implement backoff
```

## Emergency Fixes

### Can't fix pronunciation?
1. Phonetic respelling with creative spelling
2. Record custom audio for problematic word
3. Use different synonym
4. Break into syllables with dashes

### Need immediate quality improvement?
1. Switch to Multilingual v2
2. Increase stability to 60
3. Set similarity to 75
4. Regenerate multiple times

### Real-time not fast enough?
1. Flash v2.5 only option
2. Disable all normalization
3. Minimize text length
4. Use caching aggressively

## Prevention Checklist

Before generating:
- [ ] Text normalized properly
- [ ] Model appropriate for use case
- [ ] Character count within limits
- [ ] Voice settings documented
- [ ] Break tags minimal
- [ ] Segments <800 characters

After issues:
- [ ] Document problem and solution
- [ ] Update preprocessing pipeline
- [ ] Add to pronunciation dictionary
- [ ] Adjust voice settings
- [ ] Test with multiple generations
