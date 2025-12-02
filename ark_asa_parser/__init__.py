"""
ARK: Survival Ascended Save Parser
Extract player, tribe, and server data from ARK ASA save files.
"""

__version__ = "0.1.5"

from .save_reader import ArkSaveReader, scan_all_servers, PlayerData, TribeData
from .levels import xp_to_level, load_xp_table
from .xp_data import get_default_xp_table

# Async support (optional - requires aiofiles)
try:
    from .async_reader import AsyncArkSaveReader, async_scan_all_servers
    _has_async = True
except ImportError:
    _has_async = False
    AsyncArkSaveReader = None
    async_scan_all_servers = None

__all__ = [
    'ArkSaveReader',
    'scan_all_servers',
    'PlayerData',
    'TribeData',
    'xp_to_level',
    'load_xp_table',
    'get_default_xp_table',
    'AsyncArkSaveReader',
    'async_scan_all_servers',
]
