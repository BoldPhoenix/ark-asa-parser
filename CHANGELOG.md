# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2025-12-01

### Added
- Full UE5 property extraction implementation
- Player name extraction from binary save files
- Character name extraction
- Tribe name extraction from binary save files
- Tribe member list extraction (names and IDs)
- Array property parsing (StrProperty, UInt32Property arrays)
- Simple property reader module for efficient byte-pattern searching
- Comprehensive documentation with examples
- Example scripts for common use cases

### Changed
- Improved property extraction to handle UE5 binary format correctly
- Better error handling for corrupted or missing save files
- Updated README with detailed usage examples

### Fixed
- String property reading now correctly handles null terminators
- Array property parsing now accounts for proper UE5 structure layout
- Property type detection improved for reliable extraction

## [0.1.0] - 2024-12-XX

### Added
- Initial release
- Basic ARK ASA save file reading
- SQLite database parsing for world saves
- Player profile file detection (.arkprofile)
- Tribe file detection (.arktribe)
- Multi-server cluster scanning
- PlayerData and TribeData dataclasses
- Basic database info retrieval
- Server scanning functionality

### Known Limitations
- Limited property extraction in v0.1.0
- No support for FloatProperty, StructProperty, ObjectProperty yet
- Level calculation not implemented (shows placeholder value)
- Dino and structure data not yet supported

## [Unreleased]

### Planned
- FloatProperty parser for stats (health, stamina, weight)
- DoubleProperty parser
- StructProperty parser for nested data
- ObjectProperty parser for entity references
- Dino data extraction
- Structure/building data extraction
- Inventory parsing
- Level calculation from experience points
- Player stat extraction (health, stamina, weight, etc.)
- Achievement/explorer note tracking
- Engram unlock tracking

### Under Consideration
- Async file reading for performance
- Caching layer for repeated reads
- Export to JSON/CSV functionality
- Web API server mode
- Real-time save file monitoring
- Backup metadata extraction

## 0.1.2 - 2025-12-02
- Add Float/Double property parsing in simple reader
- Populate player experience from profile files (ExperiencePoints/Experience/XP)
- Attempt to read player level from CharacterLevel/PlayerLevel when present
- Prep for future stats/inventory with improved primitives
