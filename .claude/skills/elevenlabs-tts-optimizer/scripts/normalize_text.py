#!/usr/bin/env python3
"""
Text normalization script for ElevenLabs TTS optimization.
Converts numbers, symbols, abbreviations, and special formats to spoken form.
"""

import re
import argparse
import sys
from typing import Dict, List, Tuple

class TextNormalizer:
    """Comprehensive text normalizer for ElevenLabs TTS."""
    
    def __init__(self, model: str = "multilingual"):
        """Initialize normalizer with model-specific settings."""
        self.model = model.lower()
        self.setup_patterns()
        
    def setup_patterns(self):
        """Setup regex patterns and replacement dictionaries."""
        
        # Common abbreviations
        self.abbreviations = {
            "Dr.": "Doctor",
            "Mr.": "Mister",
            "Mrs.": "Missus",
            "Ms.": "Miss",
            "Prof.": "Professor",
            "St.": "Street",
            "Ave.": "Avenue",
            "Rd.": "Road",
            "Blvd.": "Boulevard",
            "Apt.": "Apartment",
            "Inc.": "Incorporated",
            "Corp.": "Corporation",
            "Ltd.": "Limited",
            "Co.": "Company",
            "Jr.": "Junior",
            "Sr.": "Senior",
            "Ph.D.": "P H D",
            "M.D.": "M D",
            "B.A.": "B A",
            "M.A.": "M A",
            "B.S.": "B S",
            "M.S.": "M S",
            "vs.": "versus",
            "etc.": "et cetera",
            "i.e.": "that is",
            "e.g.": "for example",
            "Jan.": "January",
            "Feb.": "February",
            "Mar.": "March",
            "Apr.": "April",
            "Aug.": "August",
            "Sept.": "September",
            "Oct.": "October",
            "Nov.": "November",
            "Dec.": "December",
        }
        
        # Technical abbreviations
        self.tech_abbreviations = {
            "API": "A P I",
            "URL": "U R L",
            "HTML": "H T M L",
            "CSS": "C S S",
            "SQL": "S Q L",
            "XML": "X M L",
            "JSON": "J S O N",
            "HTTP": "H T T P",
            "HTTPS": "H T T P S",
            "FTP": "F T P",
            "SSH": "S S H",
            "DNS": "D N S",
            "IP": "I P",
            "TCP": "T C P",
            "UDP": "U D P",
            "GPU": "G P U",
            "CPU": "C P U",
            "RAM": "R A M",
            "ROM": "R O M",
            "SSD": "S S D",
            "HDD": "H D D",
            "USB": "U S B",
            "PDF": "P D F",
            # "AI" - ElevenLabs handles this naturally, no need to spell out
            "ML": "M L",
            "UI": "U I",
            "UX": "U X",
            "CEO": "C E O",
            "CTO": "C T O",
            "CFO": "C F O",
            "FAQ": "F A Q",
            "ID": "I D",
            "OK": "okay",
        }
        
        # Units of measurement
        self.units = {
            "km": "kilometers",
            "m": "meters",
            "cm": "centimeters",
            "mm": "millimeters",
            "mi": "miles",
            "ft": "feet",
            "in": "inches",
            "kg": "kilograms",
            "g": "grams",
            "mg": "milligrams",
            "lb": "pounds",
            "oz": "ounces",
            "L": "liters",
            "mL": "milliliters",
            "gal": "gallons",
            "TB": "terabytes",
            "GB": "gigabytes",
            "MB": "megabytes",
            "KB": "kilobytes",
            "mph": "miles per hour",
            "kph": "kilometers per hour",
        }
        
    def number_to_words(self, num: str) -> str:
        """Convert number string to words."""
        try:
            # Handle decimals
            if '.' in num:
                parts = num.split('.')
                whole = self.int_to_words(int(parts[0]))
                decimal = ' point ' + ' '.join([self.digit_to_word(d) for d in parts[1]])
                return whole + decimal
            else:
                return self.int_to_words(int(num))
        except:
            return num  # Return original if conversion fails
    
    def int_to_words(self, n: int) -> str:
        """Convert integer to words."""
        if n == 0:
            return "zero"
        
        ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", 
                 "sixteen", "seventeen", "eighteen", "nineteen"]
        
        def convert_hundreds(num):
            result = ""
            
            hundreds = num // 100
            if hundreds > 0:
                result += ones[hundreds] + " hundred"
                
            remainder = num % 100
            if remainder >= 20:
                tens_digit = remainder // 10
                ones_digit = remainder % 10
                if result:
                    result += " "
                result += tens[tens_digit]
                if ones_digit > 0:
                    result += "-" + ones[ones_digit]
            elif remainder >= 10:
                if result:
                    result += " "
                result += teens[remainder - 10]
            elif remainder > 0:
                if result:
                    result += " "
                result += ones[remainder]
                
            return result
        
        if n < 0:
            return "negative " + self.int_to_words(-n)
        elif n < 1000:
            return convert_hundreds(n)
        elif n < 1000000:
            thousands = n // 1000
            remainder = n % 1000
            result = convert_hundreds(thousands) + " thousand"
            if remainder > 0:
                result += " " + convert_hundreds(remainder)
            return result
        elif n < 1000000000:
            millions = n // 1000000
            remainder = n % 1000000
            result = self.int_to_words(millions) + " million"
            if remainder > 0:
                result += " " + self.int_to_words(remainder)
            return result
        elif n < 1000000000000:
            billions = n // 1000000000
            remainder = n % 1000000000
            result = self.int_to_words(billions) + " billion"
            if remainder > 0:
                result += " " + self.int_to_words(remainder)
            return result
        else:
            return str(n)  # Very large numbers
    
    def digit_to_word(self, digit: str) -> str:
        """Convert single digit to word."""
        digits = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'
        }
        return digits.get(digit, digit)
    
    def normalize_currency(self, text: str) -> str:
        """Normalize currency values."""
        # Dollar amounts
        text = re.sub(r'\$([0-9,]+)\.([0-9]{2})', 
                     lambda m: self.number_to_words(m.group(1).replace(',', '')) + 
                     ' dollars and ' + self.number_to_words(m.group(2)) + ' cents', text)
        text = re.sub(r'\$([0-9,]+)', 
                     lambda m: self.number_to_words(m.group(1).replace(',', '')) + ' dollars', text)
        
        # Other currencies
        text = re.sub(r'€([0-9,]+)', 
                     lambda m: self.number_to_words(m.group(1).replace(',', '')) + ' euros', text)
        text = re.sub(r'£([0-9,]+)', 
                     lambda m: self.number_to_words(m.group(1).replace(',', '')) + ' pounds', text)
        text = re.sub(r'¥([0-9,]+)', 
                     lambda m: self.number_to_words(m.group(1).replace(',', '')) + ' yen', text)
        
        return text
    
    def normalize_phone(self, text: str) -> str:
        """Normalize phone numbers with pauses."""
        # US format
        text = re.sub(r'(\d{3})-(\d{3})-(\d{4})',
                     lambda m: ' '.join([self.digit_to_word(d) for d in m.group(1)]) + ', ' +
                     ' '.join([self.digit_to_word(d) for d in m.group(2)]) + ', ' +
                     ' '.join([self.digit_to_word(d) for d in m.group(3)]), text)
        
        # International format
        text = re.sub(r'\+(\d+) (\d+) (\d+)',
                     lambda m: 'plus ' + ' '.join([self.digit_to_word(d) for d in m.group(1)]) + ', ' +
                     ' '.join([self.digit_to_word(d) for d in m.group(2)]) + ', ' +
                     ' '.join([self.digit_to_word(d) for d in m.group(3)]), text)
        
        return text
    
    def normalize_dates(self, text: str) -> str:
        """Normalize date formats."""
        months = {
            '01': 'January', '02': 'February', '03': 'March', '04': 'April',
            '05': 'May', '06': 'June', '07': 'July', '08': 'August',
            '09': 'September', '10': 'October', '11': 'November', '12': 'December'
        }
        
        # MM/DD/YYYY format
        text = re.sub(r'(\d{1,2})/(\d{1,2})/(\d{4})',
                     lambda m: months.get(m.group(1).zfill(2), m.group(1)) + ' ' +
                     self.ordinal(int(m.group(2))) + ', ' +
                     self.year_to_words(m.group(3)), text)
        
        # YYYY-MM-DD format
        text = re.sub(r'(\d{4})-(\d{2})-(\d{2})',
                     lambda m: months.get(m.group(2), m.group(2)) + ' ' +
                     self.ordinal(int(m.group(3))) + ', ' +
                     self.year_to_words(m.group(1)), text)
        
        return text
    
    def ordinal(self, num: int) -> str:
        """Convert number to ordinal."""
        if 10 <= num % 100 <= 20:
            suffix = 'th'
        else:
            suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(num % 10, 'th')
        return self.int_to_words(num) + suffix
    
    def year_to_words(self, year: str) -> str:
        """Convert year to spoken form."""
        y = int(year)
        if 2000 <= y <= 2099:
            if y < 2010:
                return "two thousand " + self.int_to_words(y - 2000) if y > 2000 else "two thousand"
            else:
                return "twenty " + self.int_to_words(y - 2000)
        elif 1900 <= y <= 1999:
            return "nineteen " + self.int_to_words(y - 1900)
        else:
            return self.int_to_words(y)
    
    def normalize_time(self, text: str) -> str:
        """Normalize time formats."""
        # 24-hour format
        text = re.sub(r'(\d{1,2}):(\d{2})',
                     lambda m: self.time_to_words(int(m.group(1)), int(m.group(2))), text)
        
        # With AM/PM
        text = re.sub(r'(\d{1,2}):(\d{2})\s*(AM|PM|am|pm)',
                     lambda m: self.time_to_words(int(m.group(1)), int(m.group(2))) + 
                     ' ' + m.group(3).upper(), text)
        
        return text
    
    def time_to_words(self, hour: int, minute: int) -> str:
        """Convert time to words."""
        if minute == 0:
            if hour == 0:
                return "midnight"
            elif hour == 12:
                return "noon"
            else:
                h = hour if hour <= 12 else hour - 12
                return self.int_to_words(h) + " o'clock"
        elif minute == 15:
            h = hour if hour <= 12 else hour - 12
            return "quarter past " + self.int_to_words(h)
        elif minute == 30:
            h = hour if hour <= 12 else hour - 12
            return "half past " + self.int_to_words(h)
        elif minute == 45:
            h = hour + 1 if hour < 12 else hour - 11
            return "quarter to " + self.int_to_words(h)
        else:
            h = hour if hour <= 12 else hour - 12
            if minute < 10:
                return self.int_to_words(h) + " oh " + self.int_to_words(minute)
            else:
                return self.int_to_words(h) + " " + self.int_to_words(minute)
    
    def normalize_urls(self, text: str) -> str:
        """Convert URLs to spoken form."""
        # Full URLs
        text = re.sub(r'https?://([^\s]+)',
                     lambda m: "H T T P S colon slash slash " + 
                     m.group(1).replace('.', ' dot ').replace('/', ' slash '), text)
        
        # Email addresses
        text = re.sub(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.([a-zA-Z]{2,})',
                     lambda m: m.group(1).replace('.', ' dot ') + ' at ' +
                     m.group(2).replace('.', ' dot ') + ' dot ' + m.group(3), text)
        
        # Domain names
        text = re.sub(r'(?<!\S)([a-zA-Z0-9-]+)\.([a-zA-Z]{2,})(?!\S)',
                     lambda m: m.group(1) + ' dot ' + m.group(2), text)
        
        return text
    
    def normalize_symbols(self, text: str) -> str:
        """Replace symbols with words."""
        symbols = {
            '@': ' at ',
            '#': ' hashtag ',
            '%': ' percent',
            '&': ' and ',
            '+': ' plus ',
            '=': ' equals ',
            '<': ' less than ',
            '>': ' greater than ',
            '×': ' times ',
            '÷': ' divided by ',
            '°': ' degrees',
            '™': ' trademark',
            '®': ' registered',
            '©': ' copyright',
            '±': ' plus or minus ',
            '≈': ' approximately ',
            '≤': ' less than or equal to ',
            '≥': ' greater than or equal to ',
            '≠': ' not equal to ',
            '∞': ' infinity',
            '√': ' square root of ',
            'π': ' pi',
            '∑': ' sum of ',
            '∆': ' delta',
            '∂': ' partial',
            '∫': ' integral',
            '•': ' ',  # Bullet point - remove
            '·': ' ',  # Middle dot - remove
            '…': '...',  # Keep ellipsis
        }
        
        # Remove problematic brackets
        text = text.replace('{', '').replace('}', '')
        text = text.replace('[', '').replace(']', '')
        text = text.replace('<', '').replace('>', '')
        
        for symbol, replacement in symbols.items():
            text = text.replace(symbol, replacement)
        
        return text
    
    def normalize_abbreviations(self, text: str) -> str:
        """Expand common abbreviations."""
        for abbrev, expansion in self.abbreviations.items():
            text = text.replace(abbrev, expansion)
        
        # Handle technical abbreviations if not Multilingual v2
        if self.model != "multilingual":
            for tech_abbrev, expansion in self.tech_abbreviations.items():
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(tech_abbrev) + r'\b'
                text = re.sub(pattern, expansion, text)
        
        return text
    
    def normalize_units(self, text: str) -> str:
        """Expand units of measurement."""
        for unit, expansion in self.units.items():
            # Match number followed by unit
            pattern = r'(\d+)\s*' + re.escape(unit) + r'\b'
            text = re.sub(pattern, 
                         lambda m: self.number_to_words(m.group(1)) + ' ' + expansion, text)
        
        return text
    
    def normalize_numbers(self, text: str) -> str:
        """Convert standalone numbers to words."""
        # Skip if Multilingual v2 (has built-in normalization)
        if self.model == "multilingual":
            return text
        
        # Convert percentages first
        text = re.sub(r'(\d+)%', 
                     lambda m: self.number_to_words(m.group(1)) + ' percent', text)
        
        # Convert regular numbers (but not those in dates, times, etc.)
        text = re.sub(r'\b(\d+)\b',
                     lambda m: self.number_to_words(m.group(1)), text)
        
        return text
    
    def normalize(self, text: str) -> str:
        """Apply all normalization steps in order."""
        # Order matters! Process complex patterns before simple ones
        
        # 1. Normalize currency first (contains numbers)
        text = self.normalize_currency(text)
        
        # 2. Normalize dates (contains numbers)
        text = self.normalize_dates(text)
        
        # 3. Normalize times (contains numbers)
        text = self.normalize_time(text)
        
        # 4. Normalize phone numbers
        text = self.normalize_phone(text)
        
        # 5. Normalize URLs and emails
        text = self.normalize_urls(text)
        
        # 6. Normalize units (contains numbers)
        text = self.normalize_units(text)
        
        # 7. Expand abbreviations
        text = self.normalize_abbreviations(text)
        
        # 8. Normalize remaining numbers
        text = self.normalize_numbers(text)
        
        # 9. Finally, normalize symbols
        text = self.normalize_symbols(text)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Normalize text for ElevenLabs TTS'
    )
    parser.add_argument(
        'input_file',
        help='Input text file to normalize'
    )
    parser.add_argument(
        '--model',
        choices=['v3', 'multilingual', 'flash', 'turbo'],
        default='multilingual',
        help='Target ElevenLabs model (affects normalization rules)'
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
    
    # Normalize text
    normalizer = TextNormalizer(model=args.model)
    normalized = normalizer.normalize(text)
    
    # Output results
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(normalized)
            print(f"Normalized text written to '{args.output}'", file=sys.stderr)
        except Exception as e:
            print(f"Error writing output file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(normalized)

if __name__ == '__main__':
    main()
