"""
ARK: Survival Ascended Save Parser
Extract player, tribe, and server data from ARK ASA save files.
"""

__version__ = "0.2.4"

from .save_reader import ArkSaveReader, scan_all_servers, PlayerData, TribeData
from .levels import xp_to_level, load_xp_table
from .xp_data import get_default_xp_table
from .cluster_reader import scan_cluster_folder, get_cluster_summary, ClusterTransfer
from .player_stats import PlayerStatsReader
from .dino_extractor import DinoExtractor, DinoData
from .structure_extractor import StructureExtractor, StructureData
from .save_watcher import SaveWatcher, AsyncSaveWatcher, SaveFileEvent
from .historical_tracker import HistoricalTracker, PlayerSnapshot, TribeSnapshot

# Async support (optional - requires aiofiles)
try:
    from .async_reader import AsyncArkSaveReader, async_scan_all_servers
    _has_async = True
except ImportError:
    _has_async = False
    AsyncArkSaveReader = None
    async_scan_all_servers = None

__all__ = [
    # Core
    'ArkSaveReader',
    'scan_all_servers',
    'PlayerData',
    'TribeData',
    # Levels
    'xp_to_level',
    'load_xp_table',
    'get_default_xp_table',
    # Async
    'AsyncArkSaveReader',
    'async_scan_all_servers',
    # Cluster
    'scan_cluster_folder',
    'get_cluster_summary',
    'ClusterTransfer',
    # Player Stats
    'PlayerStatsReader',
    # Dino Extraction
    'DinoExtractor',
    'DinoData',
    # Structure Extraction
    'StructureExtractor',
    'StructureData',
    # Save Watching
    'SaveWatcher',
    'AsyncSaveWatcher',
    'SaveFileEvent',
    # Historical Tracking
    'HistoricalTracker',
    'PlayerSnapshot',
    'TribeSnapshot',
]
