---
name: elevenlabs-tts-optimizer
description: Expert transcript optimization for ElevenLabs text-to-speech with model-specific formatting, pronunciation control, and voice optimization. Use when preparing transcripts for TTS generation, optimizing existing text for voice-over, formatting dialogue, normalizing technical content, fixing pronunciation issues, or creating professional-quality audio narration. Handles all ElevenLabs models (v3, Multilingual v2, Flash v2.5, Turbo v2.5) with appropriate techniques.
---

# ElevenLabs TTS Optimizer

Transform raw transcripts into perfectly formatted text for natural-sounding ElevenLabs TTS generation. This skill provides comprehensive text optimization for all ElevenLabs models with automatic normalization, pronunciation control, and voice-specific formatting.

## Quick Start

### Basic Optimization Workflow

1. **Identify the model**: Ask which ElevenLabs model will be used (v3, Multilingual v2, Flash v2.5, or Turbo v2.5)
2. **Run normalization**: Use `scripts/normalize_text.py` for automatic text preprocessing
3. **Apply model-specific formatting**: Add appropriate tags, pauses, and pronunciation controls
4. **Optimize for voice**: Adjust text based on voice characteristics and content type
5. **Test and iterate**: Generate multiple versions for v3, single for v2 models

### Essential Rules

- **ALWAYS normalize numbers**: Write "123" as "one hundred twenty-three"
- **ALWAYS expand abbreviations**: "Dr." → "Doctor", "St." → "Street"
- **ALWAYS convert symbols**: "$" → "dollars", "@" → "at", "%" → "percent"
- **NEVER use problematic characters**: Remove or replace `{ } < > [ ]`
- **KEEP segments under 800 characters**: Quality degrades beyond this threshold

## Text Normalization

### Automatic Normalization

Run the normalization script for consistent preprocessing:

```bash
python scripts/normalize_text.py input.txt > normalized.txt
```

The script handles:
- Numbers to words conversion
- Symbol replacement
- Abbreviation expansion
- URL/email phonetic spelling
- Phone number formatting
- Date/time expansion

### Manual Normalization Patterns

**Numbers:**
- `123` → `one hundred twenty-three`
- `$1,234.56` → `one thousand two hundred thirty-four dollars and fifty-six cents`
- `50%` → `fifty percent`
- `2+2=4` → `two plus two equals four`

**Phone Numbers:**
- `555-123-4567` → `five five five, one two three, four five six seven`

**Dates:**
- `01/15/2024` → `January fifteenth, twenty twenty-four`
- `2024-01-15` → `January fifteenth, twenty twenty-four`

**Times:**
- `14:30` → `two thirty PM`
- `9:23 AM` → `nine twenty-three AM`

**URLs/Emails:**
- `example.com` → `example dot com`
- `john@company.com` → `john at company dot com`
- `https://api.example.com` → `H T T P S colon slash slash A P I dot example dot com`

## Model-Specific Formatting

### Eleven v3 (Alpha) - Maximum Expressiveness

**Audio Tags:**
```
[excited] This is amazing!
[whispers] Don't tell anyone...
[laughs] That's hilarious!
[sighs] I'm so tired.
[pause] Let me think about that.
[long pause] 
[beat]
```

**Multi-Character Dialogue:**
```
Sarah: [cheerfully] Good morning!
John: [interrupting] [excited] Wait, I have news!
Sarah: [surprised] What happened?
John: [overlapping] We got the contract!
```

**Important v3 Rules:**
- Prompts must be >250 characters for consistent output
- Generate 3-5 versions and select best (non-deterministic)
- Use Instant Voice Clones or Voice Design (Professional Clones not yet optimized)
- 3,000 character limit per request

### Multilingual v2 - Best Default

**Built-in Features:**
- Automatic number normalization (no manual conversion needed)
- Handles complex monetary values correctly
- 10,000 character limit
- Supports 29 languages

**Break Tags (for pauses):**
```xml
<break time="1.5s" />  <!-- Max 3 seconds -->
```

**Traditional Dialogue (tags spoken aloud):**
```
"I can't believe it," she said angrily.
"Maybe we should wait," he whispered nervously.
```

### Flash v2.5 - Ultra-Low Latency

**Critical Requirements:**
- MUST manually normalize ALL numbers (normalization disabled by default)
- Write `$1,000,000` as `one million dollars`
- 40,000 character limit
- ~75ms latency

**Phoneme Control:**
```xml
<phoneme alphabet="cmu-arpabet" ph="T AE1 L AH0 N">talon</phoneme>
<phoneme alphabet="ipa" ph="ˈæpəl">apple</phoneme>
```

### Turbo v2.5 - Balanced Performance

- Better quality than Flash, faster than Multilingual v2
- Number normalization enabled by default
- NO phoneme tag support (unlike Flash v2.5)
- 40,000 character limit
- ~250-300ms latency

## Pause and Timing Control

### Punctuation-Based (All Models)

```
Period for full stop. Comma for brief pause, semicolon for medium pause.
Question marks add rising intonation? Exclamation points add energy!
Em-dash — creates a natural pause.
Ellipses... add hesitation and emotional weight.
```

### SSML Break Tags (v2, Flash, Turbo only)

```xml
Short pause: <break time="0.5s" />
Medium pause: <break time="1s" />
Long pause: <break time="2s" />
Maximum: <break time="3s" />
```

**WARNING:** Too many break tags cause severe instability. Use sparingly!

### Audio Tags (v3 only)

```
[pause] - Standard pause
[long pause] - Extended silence
[beat] - Dramatic timing
```

## Pronunciation Control

### Method Selection by Model

| Method | v3 | Multilingual v2 | Flash v2.5 | Turbo v2.5 |
|--------|-------|-----------------|------------|------------|
| Audio tags | ✅ | ❌ | ❌ | ❌ |
| Phoneme tags | ❌ | ❌ | ✅ | ❌ |
| Break tags | ❌ | ✅ | ✅ | ✅ |
| Phonetic respelling | ✅ | ✅ | ✅ | ✅ |
| Pronunciation dictionary | ✅ | ✅ | ✅ | ✅ |

### Phoneme Tags (Flash v2.5 only)

**CMU Arpabet (recommended):**
```xml
<phoneme alphabet="cmu-arpabet" ph="AE1 P AH0 L">Apple</phoneme>
```

**Critical:** Include stress markers (1=primary, 0=unstressed)

### Phonetic Respelling (All Models)

- Capitals for emphasis: `trapezIi` (emphasize final syllables)
- Dashes for separation: `re-cord` (emphasize first syllable)
- Spaces for acronyms: `FBI` → `F B I`

### Pronunciation Dictionary

Create `.PLS` file for recurring terms:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<lexicon version="1.0" 
         xmlns="http://www.w3.org/2005/01/pronunciation-lexicon"
         alphabet="cmu-arpabet" 
         xml:lang="en-US">
  <lexeme>
    <grapheme>ElevenLabs</grapheme>
    <phoneme>IH0 L EH1 V AH0 N L AE1 B Z</phoneme>
  </lexeme>
  <lexeme>
    <grapheme>API</grapheme>
    <alias>A P I</alias>
  </lexeme>
</lexicon>
```

## Content Type Optimization

### Dialogue Formatting

Use `scripts/format_dialogue.py` for automatic formatting:

```bash
python scripts/format_dialogue.py dialogue.txt --model v3
```

**v3 Format:**
```
Character: [emotion] Dialogue text
```

**v2 Format:**
```
"Dialogue text," character said emotionally.
```

### Technical Documentation

- Spell out EVERY number and symbol
- Expand ALL abbreviations
- Use letter-by-letter for acronyms: `API` → `A P I` (exception: `AI` is pronounced naturally)
- Phone numbers with pause groupings
- URLs phonetically spelled

### Narrative/Audiobook

- Natural, book-like prose
- Proper punctuation for rhythm
- Keep segments under 800 characters
- Use Multilingual v2 for best quality

### Lists and Instructions

Convert visual formatting to verbal:

```
Bad: 1. First step
     2. Second step

Good: First, complete this step. Second, move to the next step.
```

## Voice Settings Optimization

### Stability (0-100, default 50)
- **30-45**: Expressive, varied (drama, storytelling)
- **50-60**: Balanced (general content)
- **60-75**: Consistent, controlled (technical, corporate)

### Similarity/Clarity (0-100, default 75)
- **70-80**: Optimal for most content
- Higher values may reproduce training artifacts

### Style Exaggeration (0-100, default 0)
- Keep at 0 for most applications
- Increases latency and reduces stability

### Content-Specific Settings

| Content Type | Model | Stability | Similarity | Speed |
|-------------|-------|-----------|------------|-------|
| Technical/Corporate | Multilingual v2 | 60-75 | 75-80 | 1.0 |
| Storytelling/Drama | v3 or Multilingual v2 | 30-45 | 70-80 | 0.9-1.0 |
| Real-time Agents | Flash v2.5 | 50 | 75 | 1.0 |
| Audiobooks | Multilingual v2 | 55-70 | 75-80 | 0.9 |
| Educational | Multilingual v2 | 60-70 | 75-80 | 0.8-0.9 |

## Quality Optimization Checklist

### Pre-Generation
- [ ] All numbers written as words
- [ ] Symbols converted to words
- [ ] Abbreviations expanded
- [ ] Phone/email/URL formatted phonetically
- [ ] Proper punctuation throughout
- [ ] Segments under 800 characters
- [ ] Model-appropriate formatting applied
- [ ] Voice settings optimized for content

### Post-Generation
- [ ] Check for mispronunciations
- [ ] Verify pacing feels natural
- [ ] Confirm emotional tone matches intent
- [ ] Listen for audio artifacts
- [ ] Validate pauses sound natural

## Scripts Usage

### Text Normalization
```bash
# Basic normalization
python scripts/normalize_text.py input.txt > output.txt

# With specific model optimization
python scripts/normalize_text.py input.txt --model flash
```

### Dialogue Formatting
```bash
# Format for v3 with audio tags
python scripts/format_dialogue.py dialogue.txt --model v3

# Format for v2 with traditional tags
python scripts/format_dialogue.py dialogue.txt --model v2
```

## Additional Resources

For detailed information, see:
- **Model Selection Guide**: `references/model-selection.md`
- **Voice Settings Guide**: `references/voice-settings.md`
- **Troubleshooting**: `references/troubleshooting.md`
- **Quick Reference**: `references/quick-reference.md`

## Critical Warnings

1. **NEVER use excessive break tags** - Causes severe AI instability
2. **ALWAYS normalize for Flash v2.5** - No automatic normalization
3. **NEVER exceed character limits** - v3: 3,000, Multilingual v2: 10,000, Flash/Turbo: 40,000
4. **ALWAYS test v3 multiple times** - Non-deterministic output
5. **NEVER use curly braces, angle brackets, or square brackets** - Causes artifacts
