# ARK: Survival Ascended Save Parser

A Python library for extracting player, tribe, and server data from ARK: Survival Ascended save files.

## Features

**Player Data Extraction**
- Player names (Epic Games account names)
- Character names (in-game names)
- Tribe membership
- Player levels and full stats (health, stamina, weight, etc.)

**Tribe Data Extraction**
- Tribe names
- Tribe owner information
- Member lists with names and IDs
- Tribe logs

**Server Analytics**
- Player counts across servers
- Tribe statistics
- Save file metadata
- Multi-server cluster support

**Advanced Features (v0.2.0)**
- Tamed dino extraction from world saves
- Structure/building data extraction
- Real-time save file monitoring
- Historical data tracking and analytics

## What's New

### Version 0.2.0 - Feature Complete Release
- **Dino Extraction** - Extract all tamed dinos with species, level, stats, owner info
- **Structure Extraction** - Parse buildings with categories (Storage, Defense, Crafting, etc.)
- **Real-time Save Watching** - Monitor save directory for changes with callbacks
- **Historical Tracking** - SQLite-based analytics for player progression, tribe growth
- **Full Player Stats** - Health, stamina, weight, oxygen, food, water, melee, speed

### Version 0.1.9
- **Full Player Stats** - Extract all character stats from save files
- **PlayerStatsReader** - Dedicated class for stat extraction

### Version 0.1.7
- **Cluster Transfers** - Parse ClusterObjects folder for uploaded items/dinos/characters
- **Transfer Tracking** - `scan_cluster_folder()` categorizes transfers by type
- **Cluster Statistics** - `get_cluster_summary()` for storage metrics

### Version 0.1.6
- **Performance Tools** - Profiling, benchmarking, and optimization utilities
- **Memory-Mapped Files** - `OptimizedReader` for large files (>50MB)

### Version 0.1.5
- **Async Support** - New AsyncArkSaveReader for non-blocking file I/O
- **Discord Bot Friendly** - Perfect for Discord.py with sync methods

### Version 0.1.4
- **Bundled Default XP Table** - No external JSON required
- **Enhanced Inventory Parser** - Full struct array parsing

## Installation

```bash
pip install ark-asa-parser
```

For async support:
```bash
pip install ark-asa-parser[async]
```

## Quick Start

```python
from ark_asa_parser import ArkSaveReader
from pathlib import Path

# Initialize reader with path to save directory
save_dir = Path("SavedArks/TheIsland_WP")
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

## Dino Extraction

```python
from ark_asa_parser import DinoExtractor
from pathlib import Path

world_ark = Path("SavedArks/TheIsland_WP/TheIsland_WP.ark")

# Get all tamed dinos
dinos = DinoExtractor.extract_dinos_from_world(world_ark)

for dino in dinos:
    print(f"{dino.species_name} - Level {dino.level}")
    if dino.dino_name:
        print(f"  Name: {dino.dino_name}")
    if dino.owner_name:
        print(f"  Owner: {dino.owner_name}")

# Get dino species summary
summary = DinoExtractor.get_dino_summary(world_ark)
for species, count in summary.items():
    print(f"{species}: {count}")

# Get dinos for a specific tribe
tribe_dinos = DinoExtractor.get_tribe_dinos(world_ark, tribe_id=123456)
```

## Structure Extraction

```python
from ark_asa_parser import StructureExtractor
from pathlib import Path

world_ark = Path("SavedArks/TheIsland_WP/TheIsland_WP.ark")

# Get all structures
structures = StructureExtractor.extract_structures_from_world(world_ark)

# Get structure summary with categories
summary = StructureExtractor.get_structure_summary(world_ark)
print(f"Total structures: {summary['total']}")
for category, count in summary['by_category'].items():
    print(f"  {category}: {count}")

# Get structures for a tribe
tribe_structures = StructureExtractor.get_tribe_structures(world_ark, tribe_id=123456)
```

## Real-time Save Watching

```python
from ark_asa_parser import SaveWatcher, AsyncSaveWatcher
from pathlib import Path

# Thread-based watching
save_dir = Path("SavedArks/TheIsland_WP")

def on_change(event):
    print(f"[{event.event_type}] {event.file_path.name}")
    if event.player_id:
        print(f"  Player: {event.player_id}")

watcher = SaveWatcher(save_dir, poll_interval=10.0)
watcher.add_callback(on_change)
watcher.start()

# For Discord bots - use AsyncSaveWatcher
async def setup_watcher(bot):
    async def on_player_join(event):
        if event.event_type == 'player_join':
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(f"Player joined: {event.player_id}")
    
    watcher = AsyncSaveWatcher(save_dir)
    watcher.add_callback(on_player_join)
    await watcher.start()
```

## Historical Tracking

```python
from ark_asa_parser import HistoricalTracker, PlayerSnapshot
from pathlib import Path
from datetime import datetime

# Initialize tracker with SQLite database
tracker = HistoricalTracker(Path("ark_history.db"))

# Record player snapshots
snapshot = PlayerSnapshot(
    timestamp=datetime.now(),
    eos_id="player_eos_id",
    player_name="PlayerName",
    character_name="CharName",
    level=85,
    experience=1234567.0,
    tribe_id=123456,
    server_name="TheIsland"
)
tracker.record_player_snapshot(snapshot)

# Get player progression over time
progression = tracker.get_player_level_progression("player_eos_id")

# Get top level gainers
top_players = tracker.get_top_level_gainers(days=7, limit=10)

# Get server population history
population = tracker.get_server_population_history("TheIsland", days=7)

# Activity summary
summary = tracker.get_activity_summary(days=7)
print(f"Unique players: {summary['unique_players']}")
```

## Full Player Stats

```python
from ark_asa_parser import PlayerStatsReader
from pathlib import Path

profile_path = Path("SavedArks/TheIsland_WP/player.arkprofile")

# Extract all character stats
stats = PlayerStatsReader.extract_player_stats(profile_path)

print(f"Health: {stats.health}")
print(f"Stamina: {stats.stamina}")
print(f"Weight: {stats.weight}")
print(f"Melee: {stats.melee_damage}")
print(f"Speed: {stats.movement_speed}")
```

## Scanning Multiple Servers

```python
from ark_asa_parser import scan_all_servers
from pathlib import Path

cluster_path = Path("R:/PhoenixArk")
servers = scan_all_servers(cluster_path)

for server_name, reader in servers.items():
    print(f"\nServer: {server_name}")
    players = reader.get_all_players()
    tribes = reader.get_all_tribes()
    print(f"  Players: {len(players)}")
    print(f"  Tribes: {len(tribes)}")
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

### DinoData
```python
@dataclass
class DinoData:
    species_name: str       # "Rex", "Raptor", etc.
    dino_name: str          # Custom name if set
    level: int              # Current level
    owner_name: str         # Owner player name
    tribe_id: int           # Owning tribe ID
    health: float           # Current health
    # ... and more stats
```

### StructureData
```python
@dataclass
class StructureData:
    structure_type: str     # "StorageBox", "Wall", etc.
    structure_name: str     # Custom name if set
    health: float           # Current health
    owner_name: str         # Owner name
    tribe_id: int           # Owning tribe
    is_locked: bool         # Lock status
```

## Requirements

- Python 3.8+
- No external dependencies for core features
- Optional: aiofiles for async support

## Development Status

### Implemented
- Player name and character extraction
- Tribe name and member lists
- Full player stats (health, stamina, weight, etc.)
- Tamed dino extraction from world saves
- Structure/building data extraction
- Real-time save file monitoring
- Historical data tracking and analytics
- Cluster transfer tracking
- Async support
- Performance optimization tools
- Multi-server scanning

## Contributing

Contributions are welcome! See CONTRIBUTING.md for guidelines.

## License

MIT License - See LICENSE file for details

## Credits

Developed by BoldPhoenix for the ARK: Survival Ascended community.

## Support

- **Issues**: [GitHub Issues](https://github.com/BoldPhoenix/ark-asa-parser/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BoldPhoenix/ark-asa-parser/discussions)
