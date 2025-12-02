# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-12-02

### Added
- AsyncArkSaveReader class for non-blocking async file I/O
- sync_get_all_players() and sync_get_all_tribes() methods
- sync_read_profile_file() and sync_read_tribe_file() for individual files
- sync_scan_all_servers() for cluster-wide async scanning
- sync_read_player_inventory() for async inventory reading
- Optional iofiles dependency (install with [async] extra)
- Concurrent file processing with asyncio.gather()
- Example script examples/async_usage.py with Discord bot patterns

### Changed
- Async methods process files concurrently for better performance
- CPU-bound parsing runs in executor to avoid blocking event loop

### Fixed
- Large save file reads no longer block async applications

## [0.1.4] - 2025-12-02

### Added
- Bundled default ASA XP table in xp_data.py module - no external JSON required
- Enhanced inventory parser (inventory_reader_v2.py) with full StructProperty array parsing
- Support for item quality, durability, custom names, blueprints, engrams
- Export get_default_xp_table() for users who want the bundled table

### Changed
- xp_to_level() now uses bundled default XP table when xp_table=None
- Inventory parsing improved with struct-based approach (fallback to heuristic)

### Fixed
- Level calculation no longer requires external JSON configuration

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

## 0.1.3 - 2025-12-02
- Add XP table JSON loader; ArkSaveReader accepts xp_table and computes level from experience when needed
- Inventory prototype prefers CustomItemName; expose read_player_inventory
- Add dino/structure stubs and best-effort tribe dino count
- Docs updates


### Version 0.1.6 (2025-12-02)
- Added performance utilities module (\rk_asa_parser.performance\)
- Profiling tools: \profile_function()\ for identifying bottlenecks
- Memory-mapped file access: \mmap_file()\ and \OptimizedReader\ for large files (>50MB)
- Benchmark utilities: \enchmark_file_read()\ for comparing read methods
- Optimization recommendations: \get_optimization_recommendations()\ for file-specific advice
- Created \examples/performance_testing.py\ with profiling and benchmarking examples

### Version 0.1.7 (2025-12-02)
- Added cluster transfer support (\rk_asa_parser.cluster_reader\)
- New functions: \scan_cluster_folder()\, \get_cluster_summary()\, \get_player_cluster_data()\
- ClusterTransfer dataclass for transferred characters, items, and dinos
- Parse ClusterObjects folder to track uploads between servers
- Created \examples/cluster_transfers.py\ with usage examples
- Discord bot integration example for cluster status commands

### Version 0.1.8 (2025-12-02)
- Updated README feature status to reflect completed items
- Moved inventory parsing, level calculation, async support, performance tools, and cluster transfers to 'Implemented' section
- Clarified 'In Development' items (deep UE5 parsing, real-time watching, historical tracking)
- Documentation accuracy improvements

