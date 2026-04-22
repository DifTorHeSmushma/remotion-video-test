#!/usr/bin/env python3
"""
Dialogue formatting script for ElevenLabs TTS.
Converts dialogue to appropriate format for v3 (audio tags) or v2 (traditional tags).
"""

import re
import argparse
import sys
from typing import List, Tuple, Dict

class DialogueFormatter:
    """Format dialogue for different ElevenLabs models."""
    
    def __init__(self, model: str = "v3"):
        """Initialize formatter with model-specific settings."""
        self.model = model.lower()
        self.setup_emotions()
    
    def setup_emotions(self):
        """Setup emotion mappings and patterns."""
        # Common emotions and their v3 audio tags
        self.v3_emotions = {
            'happy': '[cheerfully]',
            'cheerful': '[cheerfully]',
            'excited': '[excited]',
            'sad': '[sadly]',
            'angry': '[angry]',
            'annoyed': '[annoyed]',
            'frustrated': '[frustrated]',
            'nervous': '[nervously]',
            'worried': '[worried]',
            'surprised': '[surprised]',
            'shocked': '[shocked]',
            'confused': '[confused]',
            'thoughtful': '[thoughtfully]',
            'tired': '[tired]',
            'whisper': '[whispers]',
            'whispering': '[whispers]',
            'shout': '[shouts]',
            'shouting': '[shouts]',
            'sarcastic': '[sarcastically]',
            'laughing': '[laughs]',
            'crying': '[crying]',
            'sighing': '[sighs]',
            'gasping': '[gasps]',
            'interrupting': '[interrupting]',
            'overlapping': '[overlapping]',
            'aside': '[aside]',
            'muttering': '[muttering]',
            'quiet': '[quieter]',
            'loud': '[louder]',
            'fast': '[fast-paced]',
            'slow': '[slowly]',
            'hesitant': '[hesitates]',
        }
        
        # v2 emotion descriptors
        self.v2_emotions = {
            'happy': 'said happily',
            'cheerful': 'said cheerfully',
            'excited': 'exclaimed excitedly',
            'sad': 'said sadly',
            'angry': 'said angrily',
            'annoyed': 'said with annoyance',
            'frustrated': 'said frustratedly',
            'nervous': 'said nervously',
            'worried': 'said worriedly',
            'surprised': 'said with surprise',
            'shocked': 'said in shock',
            'confused': 'asked confusedly',
            'thoughtful': 'said thoughtfully',
            'tired': 'said tiredly',
            'whisper': 'whispered',
            'whispering': 'whispered',
            'shout': 'shouted',
            'shouting': 'shouted',
            'sarcastic': 'said sarcastically',
            'laughing': 'laughed',
            'crying': 'cried',
            'sighing': 'sighed',
            'gasping': 'gasped',
            'interrupting': 'interrupted',
            'quiet': 'said quietly',
            'loud': 'said loudly',
            'fast': 'said quickly',
            'slow': 'said slowly',
            'hesitant': 'said hesitantly',
        }
        
        # Audio effects for v3
        self.v3_effects = {
            'pause': '[pause]',
            'long_pause': '[long pause]',
            'beat': '[beat]',
            'breath': '[breath]',
            'clear_throat': '[clears throat]',
            'cough': '[coughs]',
            'sniff': '[sniffs]',
            'gulp': '[gulps]',
        }
        
        # Character voice modifiers for v3
        self.v3_voices = {
            'child': '[childlike tone]',
            'old': '[elderly voice]',
            'deep': '[deep voice]',
            'high': '[high-pitched voice]',
            'robot': '[robotic tone]',
            'pirate': '[pirate voice]',
            'british': '[British accent]',
            'french': '[French accent]',
            'southern': '[Southern drawl]',
            'new_york': '[New York accent]',
        }
    
    def parse_dialogue(self, text: str) -> List[Dict[str, str]]:
        """Parse dialogue into character, emotion, and text components."""
        lines = []
        
        # Pattern 1: "Character (emotion): dialogue"
        pattern1 = re.compile(r'^([A-Za-z\s]+)\s*\(([^)]+)\):\s*(.+)$')
        
        # Pattern 2: "Character: dialogue"
        pattern2 = re.compile(r'^([A-Za-z\s]+):\s*(.+)$')
        
        # Pattern 3: Plain dialogue with quotes
        pattern3 = re.compile(r'^"([^"]+)"(?:\s*[-—]\s*([A-Za-z\s]+))?(?:\s*\(([^)]+)\))?$')
        
        for line in text.strip().split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Try pattern 1: Character (emotion): dialogue
            match = pattern1.match(line)
            if match:
                lines.append({
                    'character': match.group(1).strip(),
                    'emotion': match.group(2).strip().lower(),
                    'text': match.group(3).strip()
                })
                continue
            
            # Try pattern 2: Character: dialogue
            match = pattern2.match(line)
            if match:
                lines.append({
                    'character': match.group(1).strip(),
                    'emotion': None,
                    'text': match.group(2).strip()
                })
                continue
            
            # Try pattern 3: "dialogue" - Character (emotion)
            match = pattern3.match(line)
            if match:
                lines.append({
                    'character': match.group(2).strip() if match.group(2) else 'Narrator',
                    'emotion': match.group(3).strip().lower() if match.group(3) else None,
                    'text': match.group(1).strip()
                })
                continue
            
            # Default: treat as narrator text
            lines.append({
                'character': 'Narrator',
                'emotion': None,
                'text': line
            })
        
        return lines
    
    def format_for_v3(self, dialogue: List[Dict[str, str]]) -> str:
        """Format dialogue with v3 audio tags."""
        formatted = []
        
        for entry in dialogue:
            line = ""
            
            # Add character name if not narrator
            if entry['character'] and entry['character'] != 'Narrator':
                line += f"{entry['character']}: "
            
            # Add emotion tag
            if entry['emotion']:
                # Try to map emotion to v3 tag
                emotion_tag = self.v3_emotions.get(entry['emotion'], f"[{entry['emotion']}]")
                line += f"{emotion_tag} "
            
            # Add dialogue text
            text = entry['text'].strip('"')  # Remove quotes if present
            
            # Look for inline emotions or effects
            text = self.add_inline_tags_v3(text)
            
            line += text
            formatted.append(line)
        
        return '\n\n'.join(formatted)
    
    def add_inline_tags_v3(self, text: str) -> str:
        """Add inline v3 audio tags based on punctuation and keywords."""
        # Add pauses for ellipses
        text = re.sub(r'\.\.\.', '[pause]', text)
        
        # Add emphasis for exclamations
        text = re.sub(r'!+', lambda m: '[excited]' if len(m.group()) > 1 else '!', text)
        
        # Add questioning tone
        text = re.sub(r'\?+', lambda m: '[confused]' if len(m.group()) > 1 else '?', text)
        
        # Add laugh indicators
        text = re.sub(r'\b(haha|hehe|lol)\b', '[laughs]', text, flags=re.IGNORECASE)
        
        # Add sigh indicators
        text = re.sub(r'\*sigh\*', '[sighs]', text, flags=re.IGNORECASE)
        
        # Add interruption markers
        text = re.sub(r'—$', '[interrupting]', text)
        
        return text
    
    def format_for_v2(self, dialogue: List[Dict[str, str]]) -> str:
        """Format dialogue with traditional v2 tags."""
        formatted = []
        
        for entry in dialogue:
            text = entry['text'].strip()
            
            # Ensure quotes around dialogue
            if not text.startswith('"'):
                text = f'"{text}"'
            
            # Add character and emotion attribution
            if entry['character'] and entry['character'] != 'Narrator':
                character = entry['character']
                
                if entry['emotion']:
                    # Use v2 emotion descriptor
                    emotion_desc = self.v2_emotions.get(entry['emotion'], f"said {entry['emotion']}ly")
                    line = f'{text} {character} {emotion_desc}.'
                else:
                    line = f'{text} {character} said.'
            else:
                # Narrator text without attribution
                line = text.strip('"')
            
            formatted.append(line)
        
        return '\n\n'.join(formatted)
    
    def add_stage_directions(self, text: str, model: str) -> str:
        """Add stage directions and effects based on model."""
        if model == "v3":
            # Add v3 effects in brackets
            text = re.sub(r'\[action: ([^\]]+)\]', r'[\1]', text)
            text = re.sub(r'\(([^)]+) happens\)', r'[\1]', text)
        else:
            # For v2, convert to narrative description
            text = re.sub(r'\[action: ([^\]]+)\]', r'(\1)', text)
        
        return text
    
    def format_multi_character_v3(self, dialogue: List[Dict[str, str]]) -> str:
        """Format multi-character dialogue for v3 with overlapping support."""
        formatted = []
        prev_character = None
        
        for i, entry in enumerate(dialogue):
            line = ""
            
            # Check for character switch
            if entry['character'] != prev_character:
                # Add character label
                line += f"{entry['character']}: "
                prev_character = entry['character']
            else:
                # Same character continuing
                line += "[continuing] "
            
            # Check for interruptions
            if i > 0 and dialogue[i-1]['text'].rstrip().endswith('—'):
                line = f"{entry['character']}: [interrupting] "
            
            # Add emotion
            if entry['emotion']:
                emotion_tag = self.v3_emotions.get(entry['emotion'], f"[{entry['emotion']}]")
                line += f"{emotion_tag} "
            
            # Add text
            line += entry['text'].strip('"')
            
            formatted.append(line)
        
        return '\n'.join(formatted)
    
    def split_long_segments(self, text: str, max_length: int = 800) -> List[str]:
        """Split text into segments under max_length characters."""
        segments = []
        current = ""
        
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for sentence in sentences:
            if len(current) + len(sentence) + 1 < max_length:
                if current:
                    current += " "
                current += sentence
            else:
                if current:
                    segments.append(current)
                current = sentence
        
        if current:
            segments.append(current)
        
        return segments
    
    def format(self, text: str) -> str:
        """Main formatting method."""
        # Parse dialogue
        dialogue = self.parse_dialogue(text)
        
        # Format based on model
        if self.model == "v3":
            formatted = self.format_for_v3(dialogue)
        elif self.model in ["v2", "multilingual", "flash", "turbo"]:
            formatted = self.format_for_v2(dialogue)
        else:
            formatted = text  # Return as-is for unknown models
        
        # Split into segments if needed
        segments = self.split_long_segments(formatted)
        
        # Add segment markers
        if len(segments) > 1:
            marked_segments = []
            for i, segment in enumerate(segments):
                marked_segments.append(f"[Segment {i+1}/{len(segments)}]\n{segment}")
            return '\n\n---\n\n'.join(marked_segments)
        
        return formatted

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Format dialogue for ElevenLabs TTS'
    )
    parser.add_argument(
        'input_file',
        help='Input dialogue file'
    )
    parser.add_argument(
        '--model',
        choices=['v3', 'v2', 'multilingual', 'flash', 'turbo'],
        default='v3',
        help='Target ElevenLabs model'
    )
    parser.add_argument(
        '--multi-character',
        action='store_true',
        help='Use multi-character v3 formatting with overlapping support'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output file (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Read input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Format dialogue
    formatter = DialogueFormatter(model=args.model)
    
    if args.multi_character and args.model == "v3":
        dialogue = formatter.parse_dialogue(text)
        formatted = formatter.format_multi_character_v3(dialogue)
    else:
        formatted = formatter.format(text)
    
    # Output results
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(formatted)
            print(f"Formatted dialogue written to '{args.output}'", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(formatted)

if __name__ == '__main__':
    main()
