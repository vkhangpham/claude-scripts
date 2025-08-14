# Implementation Plan - French-French Dictionary (Larousse)
*Started: 2025-01-14*

## Source Analysis
- **Source Type**: Feature Description + Web API Integration
- **Target Site**: https://www.larousse.fr/dictionnaires/francais/
- **Core Features**: French monolingual dictionary with definitions, etymology, expressions, citations
- **Dependencies**: requests, beautifulsoup4, rich (already available)
- **Complexity**: Medium - web scraping with rich terminal formatting

## Target Integration
- **Integration Points**: New CLI tool `lr` (Larousse) following existing patterns
- **Affected Files**: 
  - NEW: `larousse-dict.py` (main implementation)
  - NEW: `lr` (bash wrapper)
  - EXTEND: `tool_cache.py` (reuse existing caching system)
  - UPDATE: `README.md` (document new tool)
- **Pattern Matching**: Follow wordref-rich.py architecture with Rich formatting

## Current Project Patterns (Analyzed)
- **CLI Wrapper Pattern**: Bash scripts (`wr`, `cj`) that call Python implementations
- **Caching Strategy**: JSON-based persistent cache with TTL (7-30 days)
- **Rich Formatting**: Beautiful terminal tables with colors and boxes
- **Error Handling**: Graceful failures with user-friendly messages
- **Code Style**: Functional approach, clean text processing, web scraping with headers

## Implementation Tasks

### Phase 1: Core Infrastructure
- [x] ✅ Create implement directory and plan
- [x] ✅ Analyze existing project patterns
- [x] ✅ Research Larousse website structure
- [x] ✅ Create larousse-dict.py with basic structure
- [x] ✅ Create lr bash wrapper
- [x] ✅ Implement basic word lookup functionality

### Phase 2: Dictionary Features
- [x] ✅ Parse definitions with numbered sections
- [x] ✅ Extract etymology information
- [x] ✅ Capture expressions and examples
- [x] ✅ Add grammatical information (n.f., adj., etc.)
- [x] ✅ Handle synonyms and related words

### Phase 3: Rich Formatting
- [x] ✅ Design beautiful Rich table layout
- [x] ✅ Color-code different sections (definitions, etymology, expressions)
- [x] ✅ Format numbered definitions properly
- [x] ✅ Add French flag and styling consistent with other tools

### Phase 4: Caching & Performance
- [x] ✅ Integrate with existing ToolCache system
- [x] ✅ Set appropriate cache TTL (14 days for definitions)
- [x] ✅ Add cache management commands (--cache-stats, --clear-cache)
- [x] ✅ Implement proper error handling for network issues

### Phase 5: Integration & Testing
- [x] ✅ Test with various French words
- [x] ✅ Verify caching works correctly
- [x] ✅ Update README.md with usage examples
- [x] ✅ Make scripts executable and test CLI interface

## Technical Implementation Details

### URL Pattern
```
https://www.larousse.fr/dictionnaires/francais/{word}
```

### HTML Structure (Identified)
- Definitions in numbered lists
- Etymology in specific sections
- Expressions and citations in separate blocks
- Grammatical information (n.f., adj. inv., etc.)
- Synonyms with hyperlinks

### Caching Strategy
- Cache name: `larousse` 
- TTL: 14 days (longer than translations, shorter than conjugations)
- Cache key: word (normalized/lowercased)

### Rich Table Design
```
┌─────────────────────────────────────────────────────────────┐
│                    🇫🇷 Larousse: [word]                     │
├─────────────────────────────────────────────────────────────┤
│ Type: [grammatical info]                                    │
│ Étymologie: [etymology if available]                       │
├─────────────────────────────────────────────────────────────┤
│ 1. [Definition 1]                                          │
│    Synonymes: [synonyms]                                   │
│ 2. [Definition 2]                                          │
│    Synonymes: [synonyms]                                   │
├─────────────────────────────────────────────────────────────┤
│ Expressions:                                               │
│ • [expression 1]                                           │
│ • [expression 2]                                           │
└─────────────────────────────────────────────────────────────┘
```

## Validation Checklist
- [x] ✅ All core features implemented (definitions, etymology, expressions)
- [x] ✅ Caching works correctly with appropriate TTL
- [x] ✅ Error handling for network issues and missing words
- [x] ✅ Rich formatting matches project style
- [x] ✅ CLI interface consistent with existing tools
- [x] ✅ Documentation updated in README.md
- [x] ✅ Cache management commands functional
- [x] ✅ Fixed numbered list duplication issue
- [x] ✅ Created comprehensive CHANGELOG.md
- [x] ✅ Added usage examples and workflow documentation

## Risk Mitigation
- **Potential Issues**: 
  - Website structure changes
  - Rate limiting or bot detection
  - Encoding issues with French characters
  - Complex HTML parsing for different word types
- **Rollback Strategy**: Git checkpoints after each phase
- **Testing Strategy**: Test with diverse word types (nouns, verbs, adjectives, complex words)

## Success Criteria
1. ✅ User can run `lr [french_word]` to get French definitions
2. ✅ Output beautifully formatted with Rich tables
3. ✅ Caching reduces repeated network requests
4. ✅ Integrates seamlessly with existing French learning tools
5. ✅ Handles errors gracefully (network issues, word not found)
6. ✅ Documentation updated and examples provided