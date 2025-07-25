# Character Analysis Examples

This page demonstrates various ways to analyze Unicode characters and text using UICU.

## Basic Character Information

### Character Explorer

```python
import uicu

def explore_character(char):
    """Display comprehensive information about a Unicode character."""
    try:
        c = uicu.Char(char)
        
        print(f"Character: {c.value!r}")
        print(f"Code point: U+{ord(c.value):04X}")
        print(f"Name: {c.name}")
        print(f"Category: {c.category} ({c.category_name})")
        print(f"Script: {c.script} ({c.script_name})")
        print(f"Block: {c.block}")
        print(f"Direction: {c.bidirectional} ({c.bidirectional_name})")
        
        # Numeric properties
        if c.decimal is not None:
            print(f"Decimal value: {c.decimal}")
        if c.digit is not None:
            print(f"Digit value: {c.digit}")
        if c.numeric is not None:
            print(f"Numeric value: {c.numeric}")
        
        # Other properties
        if c.mirrored:
            print(f"Mirrored: Yes")
        if c.combining:
            print(f"Combining class: {c.combining}")
            
    except uicu.UICUError as e:
        print(f"Error analyzing character: {e}")

# Explore various characters
print("=== Latin Letter ===")
explore_character('A')

print("\n=== Chinese Character ===")
explore_character('中')

print("\n=== Emoji ===")
explore_character('🎉')

print("\n=== Currency Symbol ===")
explore_character('€')

print("\n=== Combining Mark ===")
explore_character('\u0301')  # Combining acute accent
```

### Character Category Analysis

```python
import uicu

def categorize_text(text):
    """Analyze character categories in text."""
    categories = {}
    
    for char in text:
        cat = uicu.category(char)
        if cat not in categories:
            categories[cat] = {
                'count': 0,
                'chars': [],
                'name': uicu.Char(char).category_name
            }
        categories[cat]['count'] += 1
        if len(categories[cat]['chars']) < 5:  # Store first 5 examples
            categories[cat]['chars'].append(char)
    
    # Display results
    print(f"Text: {text!r}")
    print(f"Total characters: {len(text)}")
    print("\nCategory breakdown:")
    
    for cat, info in sorted(categories.items()):
        examples = ''.join(info['chars'])
        print(f"  {cat} ({info['name']:25}): {info['count']:3d} - Examples: {examples!r}")

# Analyze different texts
texts = [
    "Hello, World! 123",
    "Café €25.50 (50% off!)",
    "你好世界 🌍 #Unicode",
    "الْعَرَبِيَّة",  # Arabic with diacritics
]

for text in texts:
    print("\n" + "="*60)
    categorize_text(text)
```

## Script Analysis

### Script Detection and Statistics

```python
import uicu

class ScriptAnalyzer:
    """Analyze scripts used in text."""
    
    def analyze(self, text):
        """Perform comprehensive script analysis."""
        script_stats = {}
        
        for char in text:
            script = uicu.script(char)
            script_name = uicu.script_name(script)
            
            if script not in script_stats:
                script_stats[script] = {
                    'name': script_name,
                    'count': 0,
                    'chars': set(),
                    'direction': uicu.script_direction(script)
                }
            
            script_stats[script]['count'] += 1
            script_stats[script]['chars'].add(char)
        
        # Detect primary script
        primary_script = uicu.detect_script(text)
        
        return {
            'primary': primary_script,
            'stats': script_stats,
            'mixed': len([s for s in script_stats if s not in ('Zyyy', 'Zinh')]) > 1
        }
    
    def print_analysis(self, text):
        """Print formatted analysis results."""
        results = self.analyze(text)
        
        print(f"Text: {text!r}")
        print(f"Primary script: {results['primary']}")
        print(f"Mixed scripts: {'Yes' if results['mixed'] else 'No'}")
        print("\nScript breakdown:")
        
        for script, stats in sorted(results['stats'].items(), 
                                  key=lambda x: x[1]['count'], 
                                  reverse=True):
            if script in ('Zyyy', 'Zinh'):
                continue  # Skip common/inherited
                
            print(f"\n  {script} ({stats['name']}):")
            print(f"    Count: {stats['count']}")
            print(f"    Direction: {stats['direction']}")
            print(f"    Sample chars: {''.join(list(stats['chars'])[:10])}")

# Analyze various texts
analyzer = ScriptAnalyzer()

texts = [
    "Hello World",
    "Hello мир",
    "Hello 世界 🌍",
    "مرحبا بالعالم",
    "Ελληνικά and English",
    "日本語とEnglish",
]

for text in texts:
    print("\n" + "="*60)
    analyzer.print_analysis(text)
```

### Script Transition Detection

```python
import uicu

def find_script_transitions(text):
    """Find positions where script changes in text."""
    if not text:
        return []
    
    transitions = []
    prev_script = None
    prev_char = None
    
    for i, char in enumerate(text):
        script = uicu.script(char)
        
        # Ignore common and inherited scripts
        if script in ('Zyyy', 'Zinh'):
            continue
            
        if prev_script and script != prev_script:
            transitions.append({
                'position': i,
                'from_script': prev_script,
                'to_script': script,
                'from_char': prev_char,
                'to_char': char,
                'context': text[max(0, i-5):i+6]
            })
        
        prev_script = script
        prev_char = char
    
    return transitions

# Test with mixed-script text
texts = [
    "Hello мир world",
    "Using 中文 in English text",
    "עברית and English מעורבים",
    "Switching from Ελληνικά to English and back to Ελληνικά",
]

for text in texts:
    print(f"\nText: {text!r}")
    transitions = find_script_transitions(text)
    
    if transitions:
        print("Script transitions found:")
        for t in transitions:
            from_name = uicu.script_name(t['from_script'])
            to_name = uicu.script_name(t['to_script'])
            print(f"  Position {t['position']}: {from_name} → {to_name}")
            print(f"    Context: ...{t['context']}...")
    else:
        print("No script transitions found")
```

## Advanced Character Analysis

### Grapheme Cluster Analysis

```python
import uicu

def analyze_graphemes(text):
    """Analyze grapheme clusters vs code points."""
    code_points = list(text)
    graphemes = list(uicu.graphemes(text))
    
    print(f"Text: {text!r}")
    print(f"Code points: {len(code_points)}")
    print(f"Grapheme clusters: {len(graphemes)}")
    
    if len(code_points) != len(graphemes):
        print("\nDetailed breakdown:")
        for i, g in enumerate(graphemes):
            if len(g) > 1:
                print(f"  Grapheme {i}: {g!r} ({len(g)} code points)")
                for j, cp in enumerate(g):
                    name = uicu.name(cp)
                    print(f"    {j}: U+{ord(cp):04X} {name}")

# Test with complex graphemes
test_cases = [
    "café",  # Might be é or e+́
    "👨‍👩‍👧‍👦",  # Family emoji
    "🏳️‍🌈",  # Rainbow flag
    "a\u0301\u0302",  # a + multiple combining marks
    "நி",  # Tamil character that might be decomposed
    "שָׁלוֹם",  # Hebrew with vowel points
]

for text in test_cases:
    print("\n" + "="*50)
    analyze_graphemes(text)
```

### Homograph Detection

```python
import uicu

class HomographDetector:
    """Detect potential homograph attacks in text."""
    
    # Common confusable characters
    CONFUSABLES = {
        'a': ['а', 'ɑ', 'α'],  # Latin, Cyrillic, turned, Greek
        'e': ['е', 'ё'],       # Latin, Cyrillic
        'o': ['о', 'ο', '০'],  # Latin, Cyrillic, Greek, Bengali
        'p': ['р', 'ρ'],       # Latin, Cyrillic, Greek
        'c': ['с', 'ϲ'],       # Latin, Cyrillic, Greek
        'x': ['х', 'χ'],       # Latin, Cyrillic, Greek
        'y': ['у', 'γ'],       # Latin, Cyrillic, Greek
        'i': ['і', 'ı'],       # Latin, Cyrillic, Turkish
        'l': ['І', '|', '1'],  # Lowercase L vs uppercase i, pipe, one
    }
    
    def __init__(self, allowed_scripts=None):
        self.allowed_scripts = allowed_scripts or {'Latn', 'Zyyy'}
    
    def check_text(self, text):
        """Check text for potential homographs."""
        issues = []
        
        # Check for mixed scripts
        scripts = set()
        for char in text:
            script = uicu.script(char)
            if script not in ('Zyyy', 'Zinh', 'Zzzz'):
                scripts.add(script)
        
        unexpected_scripts = scripts - self.allowed_scripts
        if unexpected_scripts:
            issues.append({
                'type': 'mixed_scripts',
                'scripts': list(scripts),
                'unexpected': list(unexpected_scripts)
            })
        
        # Check for confusable characters
        for i, char in enumerate(text.lower()):
            if char in self.CONFUSABLES:
                for confusable in self.CONFUSABLES[char]:
                    if confusable in text.lower():
                        issues.append({
                            'type': 'confusable',
                            'position': i,
                            'char': char,
                            'confusable': confusable,
                            'context': text[max(0, i-5):i+6]
                        })
        
        return {
            'safe': len(issues) == 0,
            'issues': issues,
            'scripts': list(scripts)
        }
    
    def print_report(self, text):
        """Print security report for text."""
        result = self.check_text(text)
        
        print(f"Text: {text!r}")
        print(f"Status: {'✅ SAFE' if result['safe'] else '⚠️  SUSPICIOUS'}")
        print(f"Scripts: {result['scripts']}")
        
        if result['issues']:
            print("\nIssues found:")
            for issue in result['issues']:
                if issue['type'] == 'mixed_scripts':
                    print(f"  - Mixed scripts detected: {issue['scripts']}")
                    print(f"    Unexpected: {issue['unexpected']}")
                elif issue['type'] == 'confusable':
                    print(f"  - Confusable characters: '{issue['char']}' and '{issue['confusable']}'")
                    print(f"    Context: {issue['context']}")

# Test various URLs and text
detector = HomographDetector()

test_cases = [
    "google.com",
    "gооgle.com",  # Cyrillic 'оо'
    "раypаl.com",  # Cyrillic 'ра'
    "amаzon.com",  # Cyrillic 'а'
    "microsoft.com",  # Safe
    "ebаy.com",    # Cyrillic 'а'
]

for text in test_cases:
    print("\n" + "="*50)
    detector.print_report(text)
```

### Character Normalization Analysis

```python
import uicu

def analyze_normalization(text):
    """Analyze different normalization forms of text."""
    # Create normalizers
    nfc = uicu.Transliterator('NFC')
    nfd = uicu.Transliterator('NFD')
    nfkc = uicu.Transliterator('NFKC')
    nfkd = uicu.Transliterator('NFKD')
    
    # Get normalized forms
    forms = {
        'Original': text,
        'NFC': nfc.transliterate(text),
        'NFD': nfd.transliterate(text),
        'NFKC': nfkc.transliterate(text),
        'NFKD': nfkd.transliterate(text),
    }
    
    print(f"Original text: {text!r}")
    print("\nNormalization forms:")
    
    for name, form in forms.items():
        print(f"\n{name}:")
        print(f"  Text: {form!r}")
        print(f"  Length: {len(form)} code points")
        print(f"  Graphemes: {len(list(uicu.graphemes(form)))}")
        
        if name != 'Original' and form != text:
            print("  Changed: YES")
            # Show character breakdown for changed forms
            if len(form) != len(text):
                print("  Characters:")
                for char in form:
                    print(f"    U+{ord(char):04X} {uicu.name(char)}")

# Test with various texts needing normalization
test_texts = [
    "café",  # Precomposed
    "café",  # Decomposed
    "½",     # Fraction
    "ｆｕｌｌｗｉｄｔｈ",  # Fullwidth
    "ﬁle",   # Ligature
    "Ⅻ",     # Roman numeral
    "①②③",   # Circled numbers
    "𝐇𝐞𝐥𝐥𝐨",  # Mathematical alphanumeric
]

for text in test_texts:
    print("\n" + "="*60)
    analyze_normalization(text)
```

## Practical Applications

### Smart Character Counter

```python
import uicu

class SmartCharacterCounter:
    """Count characters in user-friendly ways."""
    
    def count(self, text):
        """Perform various character counts."""
        return {
            'bytes': len(text.encode('utf-8')),
            'code_points': len(text),
            'graphemes': len(list(uicu.graphemes(text))),
            'words': len(list(uicu.words(text))),
            'sentences': len(list(uicu.sentences(text))),
            'printable': self._count_printable(text),
            'visible': self._count_visible(text),
        }
    
    def _count_printable(self, text):
        """Count printable characters."""
        count = 0
        for char in text:
            cat = uicu.category(char)
            # Exclude control and formatting characters
            if not cat.startswith('C'):
                count += 1
        return count
    
    def _count_visible(self, text):
        """Count visible characters (exclude spaces)."""
        count = 0
        for char in text:
            cat = uicu.category(char)
            # Exclude control, formatting, and space characters
            if not (cat.startswith('C') or cat.startswith('Z')):
                count += 1
        return count
    
    def print_counts(self, text):
        """Print formatted character counts."""
        counts = self.count(text)
        
        print(f"Text: {text!r}")
        print(f"UTF-8 bytes:     {counts['bytes']:4d}")
        print(f"Code points:     {counts['code_points']:4d}")
        print(f"Graphemes:       {counts['graphemes']:4d} (user-perceived characters)")
        print(f"Printable:       {counts['printable']:4d}")
        print(f"Visible:         {counts['visible']:4d} (excluding spaces)")
        print(f"Words:           {counts['words']:4d}")
        print(f"Sentences:       {counts['sentences']:4d}")

# Test with various texts
counter = SmartCharacterCounter()

test_texts = [
    "Hello, World!",
    "Family: 👨‍👩‍👧‍👦",
    "Hello\u200BWorld",  # With zero-width space
    "Test\nWith\nNewlines",
    "Mixed 中英文 text with émojis 🎉",
]

for text in test_texts:
    print("\n" + "="*50)
    counter.print_counts(text)
```

### Text Security Scanner

```python
import uicu

class TextSecurityScanner:
    """Scan text for potential security issues."""
    
    def scan(self, text):
        """Comprehensive security scan of text."""
        issues = []
        
        # Check for invisible characters
        invisible_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF', '\u200E', '\u200F']
        for char in invisible_chars:
            if char in text:
                name = uicu.name(char)
                issues.append(f"Invisible character found: {name}")
        
        # Check for mixed scripts (potential homograph)
        scripts = set()
        for char in text:
            script = uicu.script(char)
            if script not in ('Zyyy', 'Zinh', 'Zzzz'):
                scripts.add(script)
        
        if len(scripts) > 1:
            issues.append(f"Mixed scripts detected: {list(scripts)}")
        
        # Check for RTL override characters
        rtl_overrides = ['\u202A', '\u202B', '\u202C', '\u202D', '\u202E']
        for char in rtl_overrides:
            if char in text:
                name = uicu.name(char)
                issues.append(f"Bidirectional override found: {name}")
        
        # Check for unusual Unicode categories
        unusual_categories = {'Cc', 'Cf', 'Co', 'Cn'}
        for char in text:
            cat = uicu.category(char)
            if cat in unusual_categories:
                issues.append(f"Unusual character category {cat}: U+{ord(char):04X}")
        
        return {
            'safe': len(issues) == 0,
            'issues': issues,
            'scripts': list(scripts),
            'has_rtl': any(uicu.bidirectional(c) in ('R', 'AL') for c in text),
        }
    
    def print_report(self, text):
        """Print security scan report."""
        result = self.scan(text)
        
        print(f"Text: {text!r}")
        print(f"Length: {len(text)} characters")
        print(f"Status: {'✅ SAFE' if result['safe'] else '⚠️  ISSUES FOUND'}")
        print(f"Scripts: {result['scripts']}")
        print(f"Contains RTL: {'Yes' if result['has_rtl'] else 'No'}")
        
        if result['issues']:
            print("\nSecurity issues:")
            for issue in result['issues']:
                print(f"  - {issue}")

# Test various potentially problematic texts
scanner = TextSecurityScanner()

test_cases = [
    "Normal text",
    "Text with \u200B zero-width space",
    "Mixed латиница and latin",
    "Text with \u202E RTL override",
    "Clean مرحبا Arabic text",
    "Weird \uFEFF BOM character",
]

for text in test_cases:
    print("\n" + "="*50)
    scanner.print_report(text)
```

## Summary

These examples demonstrate:

1. **Character Property Analysis** - Exploring Unicode character properties
2. **Script Detection** - Identifying and analyzing writing systems
3. **Security Scanning** - Detecting potential security issues in text
4. **Normalization** - Understanding Unicode normalization forms
5. **Practical Counting** - User-friendly character counting

For more examples, see:
- [Text Processing](text-processing.md) - Text segmentation examples
- [Multilingual Sorting](multilingual-sorting.md) - Locale-aware sorting
- [Script Conversion](script-conversion.md) - Transliteration examples