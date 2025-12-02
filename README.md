# ARK: Survival Ascended Save Parser

A Python library for extracting player, tribe, and server data from ARK: Survival Ascended save files.

## Features

âœ… **Player Data Extraction**
- Player names (Epic Games account names)
- Character names (in-game names)
- Tribe membership
- Player levels and stats

âœ… **Tribe Data Extraction**
- Tribe names
- Tribe owner information
- Member lists with names and IDs
- Tribe logs

âœ… **Server Analytics**
- Player counts across servers
- Tribe statistics
- Save file metadata
- Multi-server cluster support

## What's New

### Version 0.1.7
- **Cluster Transfers** - Parse ClusterObjects folder for uploaded items/dinos/characters
- **Transfer Tracking** - `scan_cluster_folder()` categorizes transfers by type
- **Cluster Statistics** - `get_cluster_summary()` for storage metrics
- **Discord Ready** - Example commands for cluster status embeds

### Version 0.1.6
- **Performance Tools** - Profiling, benchmarking, and optimization utilities
- **Memory-Mapped Files** - `OptimizedReader` for large files (>50MB)
- **Profiling Support** - Identify bottlenecks with `profile_function()`
- **Optimization Hints** - Get file-specific recommendations

### Version 0.1.5
-  **Async Support** - New AsyncArkSaveReader for non-blocking file I/O
-  **Discord Bot Friendly** - Perfect for Discord.py with sync_get_all_players(), sync_get_all_tribes()
-  **Concurrent Processing** - Process multiple files simultaneously with asyncio.gather()
-  **Optional Dependency** - Install with pip install ark-asa-parser[async] for aiofiles support
### Version 0.1.4
-  **Bundled Default XP Table** - No external JSON required! Library now includes official ASA XP thresholds
-  **Enhanced Inventory Parser** - Full struct array parsing for item quality, durability, custom names (when inventory present)
-  **Simplified API** - xp_to_level() now works out-of-the-box without providing XP table

### Version 0.1.2 & 0.1.3
- Optional XP table support to compute level from XP
- Inventory parsing prototype (names + quantities; prefers CustomItemName)
- Tribe dino counts (best-effort from common properties)


## Installation

```bash
pip install ark-asa-parser
```

## Quick Start

```python
from ark_asa_parser import ArkSaveReader
from pathlib import Path

# Initialize reader with path to save directory
save_dir = Path("R:/PhoenixArk/asaserver_island/ShooterGame/Saved/SavedArks/TheIsland_WP")
reader = ArkSaveReader(save_dir)

# Get all players
players = reader.get_all_players()
for player in players:
    print(f"{player.player_name} ({player.character_name})")
    print(f"  Tribe ID: {player.tribe_id}")
    print(f"  Level: {player.level}")

# Get all tribes
tribes = reader.get_all_tribes()
for tribe in tribes:
    print(f"{tribe.tribe_name}")
    print(f"  Owner: {tribe.owner_name}")
    print(f"  Members: {tribe.member_count}")
```

## Scanning Multiple Servers

```python
from ark_asa_parser import scan_all_servers
from pathlib import Path

# Scan entire cluster
cluster_path = Path("R:/PhoenixArk")
servers = scan_all_servers(cluster_path)

for server_name, reader in servers.items():
    print(f"\nServer: {server_name}")
    players = reader.get_all_players()
    tribes = reader.get_all_tribes()
    print(f"  Players: {len(players)}")
    print(f"  Tribes: {len(tribes)}")
```

## File Structure

ARK ASA saves use the following structure:

```
SavedArks/
â”œâ”€â”€ MapName_WP/                    # Save directory
â”‚   â”œâ”€â”€ MapName_WP.ark            # World save (SQLite database)
â”‚   â”œâ”€â”€ <eos_id>.arkprofile       # Player profile files
â”‚   â””â”€â”€ <tribe_id>.arktribe       # Tribe data files
```

## Data Classes

### PlayerData

```python
@dataclass
class PlayerData:
    eos_id: str              # Epic Online Services ID
    player_name: str         # Epic Games account name
    character_name: str      # In-game character name
    tribe_id: int           # Tribe membership ID
    level: int              # Character level
    experience: float       # Experience points
```

### TribeData

```python
@dataclass
class TribeData:
    tribe_id: int           # Unique tribe ID
    tribe_name: str         # Tribe name
    owner_name: str         # Tribe owner identifier
    member_count: int       # Number of members
```

## Advanced Usage

### Get Server Database Info

```python
reader = ArkSaveReader(save_dir)
info = reader.get_database_info()

print(f"Tables: {info['tables']}")
print(f"File size: {info['file_size']} bytes")
print(f"Last modified: {info['file_modified']}")
```

### Read Individual Files

```python
from pathlib import Path

# Read specific player profile
player_file = Path("path/to/player.arkprofile")
player = reader.read_profile_file(player_file)

# Read specific tribe file
tribe_file = Path("path/to/tribe.arktribe")
tribe = reader.read_tribe_file(tribe_file)
```

## How It Works

The library uses a custom binary parser to extract UE5 (Unreal Engine 5) properties from ARK's save files:

1. **World Saves (.ark)**: SQLite databases containing game objects and world state
2. **Player Profiles (.arkprofile)**: Binary files with UE5 property serialization containing player data
3. **Tribe Files (.arktribe)**: Binary files with UE5 property serialization containing tribe information

The parser handles:
- Length-prefixed strings (ASCII and UTF-16)
- Various property types (String, Integer, Array)
- Nested property structures
- Binary search for efficient property extraction

## Requirements

- Python 3.8+
- No external dependencies (uses only Python standard library)

## Development Status

### âœ… Implemented
- Player name extraction
- Character name extraction
- Tribe name extraction
- Tribe member lists
- Basic player stats (level via field when available, tribe membership, experience parsing)
- Multi-server scanning

### ðŸš§ In Development
- Full player stats (health, stamina, weight, etc.)  groundwork started (Float/Double parsing)
- Dino data extraction
- Structure data extraction
- Inventory parsing (prototype: item names + quantities)
- Level calculation from experience (experience now parsed; mapping next)

## Contributing

Contributions are welcome! This is an open-source project to help the ARK community build tools for server management, analytics, and player tracking.

### Areas for Contribution
- Additional property type parsers (Float, Struct, Object)
- Dino data extraction
- Structure/building data
- Documentation improvements
- Example scripts and use cases

## License

MIT License - See LICENSE file for details

## Credits

Developed by BoldPhoenix for the ARK: Survival Ascended community.

Special thanks to the ARK modding community for reverse-engineering documentation.

## Support

- **Issues**: [GitHub Issues](https://github.com/BoldPhoenix/ark-asa-parser/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BoldPhoenix/ark-asa-parser/discussions)

## Example Use Cases

- Discord bots for server statistics
- Web dashboards for player tracking
- Automated backup systems with metadata
- Player activity monitoring
- Tribe management tools
- Server admin utilities

## Version History

### 0.1.1 (Current)
- Full property extraction implementation
- Player name and character name support
- Tribe name and member list support
- Array property parsing
- Multi-server cluster scanning

### 0.1.0
- Initial release
- Basic save file reading
- SQLite database parsing
- Player and tribe file detection





## New in 0.1.2/0.1.3
- Experience parsing via Float/Double properties; optional level from explicit fields
- Optional XP table support to compute level from XP
- Inventory parsing prototype (names + quantities; prefers CustomItemName)
- Best-effort tribe dino count field when present




## Performance Optimization

The library includes performance tools for profiling, benchmarking, and optimizing large file processing:

```python
from ark_asa_parser.performance import (
    profile_function,
    OptimizedReader,
    get_optimization_recommendations
)

# Profile to find bottlenecks
reader = ArkSaveReader(save_path)
players, stats = profile_function(reader.get_all_players)
stats.sort_stats("cumulative").print_stats(10)

# Use memory-mapped files for large saves (>50MB)
with OptimizedReader(profile_path) as reader:
    positions = reader.find_all(b"PlayerName")
    chunk = reader.read_chunk(positions[0], 100)

# Get optimization recommendations
rec = get_optimization_recommendations(profile_path)
if rec["use_mmap"]:
    print(f"File is {rec["file_size_mb"]:.1f}MB - consider mmap")
```

See `examples/performance_testing.py` for complete benchmarking examples.



