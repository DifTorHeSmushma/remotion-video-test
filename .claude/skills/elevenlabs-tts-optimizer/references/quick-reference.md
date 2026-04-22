# Quick Reference

## Essential Normalization

### Numbers
```
123 → one hundred twenty-three
$45.67 → forty-five dollars and sixty-seven cents
50% → fifty percent
1st → first
```

### Symbols
```
@ → at
# → hashtag
% → percent
& → and
$ → dollars
```

### Dates & Times
```
01/15/2024 → January fifteenth, twenty twenty-four
14:30 → two thirty PM
2024 → twenty twenty-four
```

### URLs & Emails
```
example.com → example dot com
john@company.com → john at company dot com
https:// → H T T P S colon slash slash
```

### Phone Numbers
```
555-123-4567 → five five five, one two three, four five six seven
```

## Model Quick Select

```
Need speed? → Flash v2.5
Need quality? → Multilingual v2  
Need emotion? → Eleven v3
Need balance? → Turbo v2.5
```

## Character Limits

- **v3**: 3,000
- **Multilingual v2**: 10,000
- **Flash/Turbo v2.5**: 40,000
- **Optimal segment**: <800

## Pause Control

### All Models
```
. (period) = full stop
, (comma) = brief pause
; (semicolon) = medium pause
— (em dash) = natural pause
... (ellipsis) = hesitation
```

### v2 Models Only
```xml
<break time="1s" />  <!-- 3s max -->
```

### v3 Only
```
[pause]
[long pause]
[beat]
```

## v3 Audio Tags

### Emotions
```
[excited] [happy] [sad] [angry]
[nervous] [confused] [surprised]
[thoughtful] [tired] [frustrated]
```

### Delivery
```
[whispers] [shouts] [slowly]
[fast-paced] [sarcastically]
[laughs] [sighs] [gasps]
```

### Multi-character
```
[interrupting] [overlapping]
[continuing] [aside]
```

### Accents/Voices
```
[British accent] [French accent]
[childlike tone] [deep voice]
[robotic tone] [pirate voice]
```

## Phoneme Tags (Flash v2.5 only)

```xml
<phoneme alphabet="cmu-arpabet" ph="AE1 P AH0 L">Apple</phoneme>
```
**Remember stress markers: 1=primary, 0=unstressed**

## Voice Settings

### Default
```
Stability: 50
Similarity: 75
Style: 0
Speed: 1.0
```

### Professional
```
Stability: 60-75
Similarity: 75-80
```

### Expressive
```
Stability: 30-45
Similarity: 70-80
```

## Common Fixes

| Problem | Quick Fix |
|---------|-----------|
| Numbers wrong | Use Multilingual v2 or normalize |
| Too monotone | Stability → 35-45 |
| Too variable | Stability → 60-70 |
| Tags spoken | Check using v3 model |
| Speeds up | Remove break tags |
| Accent switch | Keep <800 chars |
| Acronym wrong | Space letters: F B I |

## API Examples

### Python - Basic
```python
import requests

response = requests.post(
    "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    json={
        "text": normalized_text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 55,
            "similarity_boost": 75
        }
    },
    headers={"xi-api-key": API_KEY}
)
```

### Streaming
```python
response = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream",
    json={"text": text, "model_id": "eleven_flash_v2_5"},
    stream=True
)
```

## Preprocessing Checklist

- [ ] Numbers as words
- [ ] Symbols replaced
- [ ] Abbreviations expanded
- [ ] URLs/emails phonetic
- [ ] Under character limit
- [ ] Segments <800 chars
- [ ] Model appropriate
- [ ] Voice selected
- [ ] Settings configured

## Model Feature Matrix

| | v3 | Mult v2 | Flash | Turbo |
|-|-------|---------|--------|--------|
| Speed | Slow | Medium | Fast | Medium |
| Quality | Best* | Best | Good | Good |
| Emotion | High | Medium | Low | Low |
| Cost | 100% | 100% | 50% | 100% |
| Streaming | ❌ | ✅ | ✅ | ✅ |
| Auto-norm | ✅ | ✅ | ❌ | ✅ |

*For expressive content

## Command Line

### Normalize text
```bash
python normalize_text.py input.txt --model flash > output.txt
```

### Format dialogue
```bash
python format_dialogue.py dialogue.txt --model v3 -o formatted.txt
```

## Golden Rules

1. **Always normalize for Flash v2.5**
2. **Never exceed character limits**
3. **Keep segments under 800 chars**
4. **Generate 3-5 times for v3**
5. **Document working settings**
6. **Style exaggeration = 0**
7. **Test with actual content**
8. **Match voice to language**
9. **Cache generated audio**
10. **Higher stability for long content**

## Emergency Contacts

- API Issues: https://status.elevenlabs.io
- Documentation: https://docs.elevenlabs.io
- Support: support@elevenlabs.io
