# Claude Scripts

A collection of helpful command-line tools and scripts created with Claude's assistance.

## French Learning Tools

### WordReference Translation (`wr`)
- **Purpose**: English-French translation using WordReference.com
- **Usage**: `wr <english_word>`
- **Features**: Clean 3-column table display with context and grammatical information
- **Caching**: 7-day cache with management commands

### French Conjugation (`cj`)
- **Purpose**: Comprehensive French verb conjugation tool
- **Usage**: 
  - `cj <verb>` - All conjugations
  - `cj <person> <verb>` - All tenses for a person
  - `cj <person> <verb> <tense>` - Specific conjugation (original format)
  - `cj -<tense> <person> <verb>` - Specific conjugation (flag format)
- **Features**: 
  - Multiple aliases for tenses (e.g., `p` for présent, `f` for futur)
  - Support for all French moods and tenses
  - Beautiful terminal formatting with Rich library
- **Caching**: 30-day cache with management commands

### Pipeline Tool (`wr-cj`)
- **Purpose**: Combined English→French translation + conjugation workflow
- **Usage**: `wr-cj <english_verb> [person] [tense]`
- **Features**: Automatically extracts French verb from translation and conjugates it

### French Dictionary (`lr`)
- **Purpose**: French-French monolingual dictionary using Larousse
- **Usage**: `lr <mot_français>`
- **Features**: 
  - Complete French definitions with numbered meanings
  - Etymology and grammatical information
  - Synonyms and antonyms for each definition
  - Beautiful terminal formatting with Rich library
- **Caching**: 14-day cache with management commands

### French Pronunciation (`speak-fr`)
- **Purpose**: French text-to-speech using macOS built-in voices
- **Usage**: `speak-fr "<french_text>"`
- **Features**: Uses high-quality French voice for pronunciation

## Other Tools

### PDF Text Extractor (`pdf-extract`)
- **Purpose**: Extract text content from PDF files
- **Usage**: `pdf-extract <pdf_file>`

### Claude Live Reader (`claude-live-reader.sh`)
- **Purpose**: Live reading tool for Claude interactions
- **Usage**: `./claude-live-reader.sh`

## Technical Implementation

- **Rich Library**: Beautiful terminal formatting with colors and tables
- **verbecc**: Machine learning-based French conjugation engine
- **BeautifulSoup4**: Web scraping for WordReference translations and Larousse dictionary
- **Caching System**: JSON-based persistent caching with expiration (7-30 days depending on tool)
- **macOS Integration**: Native text-to-speech for pronunciation
- **Larousse Integration**: French monolingual dictionary with comprehensive definitions

## Installation

1. Ensure Python 3 and required packages are installed:
   ```bash
   pip install rich verbecc requests beautifulsoup4
   ```

2. Make scripts executable:
   ```bash
   chmod +x wr cj lr wr-cj speak-fr
   ```

3. Add to PATH or create aliases as needed.

## Cache Management

All tools support cache management:
- `--cache-stats`: View cache statistics for all French learning tools
- `--clear-cache`: Clear all cached data
- `--cleanup-cache`: Remove expired entries only

## Examples

### Basic French Learning Workflow
```bash
# Look up an English word
wr run
# → Shows French translations including "courir"

# Get French definitions 
lr courir
# → Shows comprehensive French definitions from Larousse

# Conjugate the French verb
cj courir
# → Shows all conjugations

# Practice pronunciation
speak-fr "je cours, tu cours, il court"
# → Speaks French with native pronunciation
```

### Pipeline Workflow
```bash
# Combined translation + conjugation
wr-cj run je p
# → Translates "run" to French, then shows "je cours"

# Check cache status
lr --cache-stats
# → Shows cache statistics for all tools
```

## Complete French Learning Toolkit

This collection provides a comprehensive French learning environment:
- **Translation**: English ↔ French with context
- **Dictionary**: French definitions and etymology  
- **Conjugation**: Complete verb forms and tenses
- **Pronunciation**: Native French audio output
- **Caching**: Offline access to previous lookups