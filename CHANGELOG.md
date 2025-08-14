# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-14

### Added
- **French Dictionary (`lr`)** - Complete French-French monolingual dictionary using Larousse
  - Numbered definitions with comprehensive French meanings
  - Etymology and grammatical information extraction
  - Synonyms and antonyms for each definition
  - Beautiful terminal formatting with French flag styling
  - 14-day intelligent caching system
  - Seamless integration with existing French learning tools
  - Cache management commands (`--cache-stats`, `--clear-cache`, `--cleanup-cache`)
  - Error handling for network issues and missing words
- Enhanced shared caching system to support Larousse dictionary
- Updated cache statistics to include all French learning tools

### Changed
- Extended `tool_cache.py` to include Larousse in unified cache management
- Updated installation instructions to include new `lr` tool
- Enhanced documentation with comprehensive French dictionary usage examples

### Technical Details
- **New Files**: `larousse-dict.py`, `lr` (bash wrapper)
- **Dependencies**: Uses existing Rich, BeautifulSoup4, requests libraries
- **Architecture**: Follows established CLI wrapper → Python implementation pattern
- **Caching Strategy**: 14-day TTL optimized for dictionary definitions
- **URL Pattern**: `https://www.larousse.fr/dictionnaires/francais/{word}`

## [1.0.0] - Initial Release

### Added
- **WordReference Translation (`wr`)** - English-French translation with 7-day caching
- **French Conjugation (`cj`)** - Comprehensive verb conjugation with 30-day caching
- **Pipeline Tool (`wr-cj`)** - Combined translation and conjugation workflow
- **French Pronunciation (`speak-fr`)** - macOS text-to-speech integration
- **PDF Text Extractor (`pdf-extract`)** - Extract text from PDF files
- **Claude Live Reader** - Live reading tool for Claude interactions
- **Shared Caching System** - JSON-based persistent caching with TTL
- **Rich Terminal Formatting** - Beautiful tables, colors, and styling
- **Cache Management** - Unified commands across all tools