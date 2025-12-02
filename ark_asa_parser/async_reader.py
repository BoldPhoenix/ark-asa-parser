"""
Async wrappers for ARK ASA save file reading.
Use these for Discord bots and async applications to avoid blocking.
"""
import asyncio
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    import aiofiles
    HAS_AIOFILES = True
except ImportError:
    HAS_AIOFILES = False

from .save_reader import ArkSaveReader, PlayerData, TribeData
from .simple_property_reader import extract_player_data_simple, extract_tribe_data_simple
from .levels import xp_to_level
from .inventory_reader import read_inventory_from_profile
from .dino_structure import try_get_tribe_dino_count


class AsyncArkSaveReader:
    """
    Async version of ArkSaveReader for non-blocking file I/O.
    
    Requires: pip install aiofiles
    
    Usage:
        reader = AsyncArkSaveReader(save_dir)
        players = await reader.async_get_all_players()
    """
    
    def __init__(self, save_dir: Path, xp_table: Optional[List[float]] = None):
        """
        Initialize async reader.
        
        Args:
            save_dir: Path to SavedArks directory
            xp_table: Optional XP threshold table (uses default if None)
        """
        if not HAS_AIOFILES:
            raise ImportError(
                "aiofiles is required for async reading. "
                "Install with: pip install aiofiles"
            )
        
        self.save_dir = Path(save_dir)
        self.world_save = self.save_dir / f"{self.save_dir.name}.ark"
        self.xp_table = xp_table
        
        # Fallback sync reader for methods that need it
        self._sync_reader = ArkSaveReader(save_dir, xp_table)
    
    def is_valid(self) -> bool:
        """Check if save directory exists (sync - file check is fast)"""
        return self._sync_reader.is_valid()
    
    async def get_database_info(self) -> Dict:
        """Get basic save database info (runs in executor to avoid blocking)"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_reader.get_database_info)
    
    async def list_profile_files(self) -> List[Path]:
        """List all .arkprofile files (fast directory scan, run in executor)"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_reader.list_profile_files)
    
    async def list_tribe_files(self) -> List[Path]:
        """List all .arktribe files"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._sync_reader.list_tribe_files)
    
    async def async_read_profile_file(self, profile_path: Path) -> Optional[PlayerData]:
        """
        Async read of .arkprofile file with non-blocking I/O.
        """
        if not profile_path.exists():
            return None
        
        try:
            player = PlayerData()
            player.file_path = str(profile_path)
            player.eos_id = profile_path.stem
            
            # Get file stats (fast)
            file_stat = profile_path.stat()
            player.last_seen = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Read file data async
            async with aiofiles.open(profile_path, 'rb') as f:
                data = await f.read()
            
            # Parse in executor (CPU-bound)
            loop = asyncio.get_event_loop()
            player_data = await loop.run_in_executor(
                None,
                extract_player_data_simple,
                profile_path,
                player.eos_id
            )
            
            if player_data:
                player.player_name = player_data.get('player_name', '')
                player.character_name = player_data.get('character_name', '')
                player.tribe_id = player_data.get('tribe_id')
                player.level = player_data.get('level', 1)
                player.experience = player_data.get('experience', 0.0)
                
                # Compute level from XP if needed
                if (player.level <= 1 or player.level is None) and player.experience > 0:
                    computed_level = xp_to_level(player.experience, self.xp_table)
                    if computed_level:
                        player.level = computed_level
            
            return player
            
        except Exception as e:
            print(f"Error reading profile {profile_path}: {e}")
            return None
    
    async def async_read_tribe_file(self, tribe_path: Path) -> Optional[TribeData]:
        """
        Async read of .arktribe file.
        """
        if not tribe_path.exists():
            return None
        
        try:
            tribe_id = int(tribe_path.stem)
            tribe = TribeData(tribe_id=tribe_id)
            tribe.file_path = str(tribe_path)
            
            file_stat = tribe_path.stat()
            tribe.last_active = datetime.fromtimestamp(file_stat.st_mtime)
            
            # Read file async
            async with aiofiles.open(tribe_path, 'rb') as f:
                data = await f.read()
            
            # Parse in executor
            loop = asyncio.get_event_loop()
            tribe_data = await loop.run_in_executor(
                None,
                extract_tribe_data_simple,
                tribe_path,
                tribe_id
            )
            
            if tribe_data:
                tribe.tribe_name = tribe_data.get('tribe_name', '')
                tribe.owner_name = f"ID:{tribe_data.get('owner_id', 0)}"
                members = tribe_data.get('members', [])
                tribe.member_count = len(members)
            
            # Try to get dino count
            dino_count = await loop.run_in_executor(
                None,
                try_get_tribe_dino_count,
                tribe_path
            )
            if dino_count is not None and dino_count > 0:
                tribe.dino_count = dino_count
            
            return tribe
            
        except Exception as e:
            print(f"Error reading tribe {tribe_path}: {e}")
            return None
    
    async def async_get_all_players(self) -> List[PlayerData]:
        """
        Get all player data with async file I/O.
        Processes files concurrently for better performance.
        """
        profile_files = await self.list_profile_files()
        
        # Process all profiles concurrently
        tasks = [self.async_read_profile_file(pf) for pf in profile_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out None and exceptions
        players = []
        for result in results:
            if isinstance(result, PlayerData):
                players.append(result)
        
        return players
    
    async def async_get_all_tribes(self) -> List[TribeData]:
        """
        Get all tribe data with async file I/O.
        Processes files concurrently.
        """
        tribe_files = await self.list_tribe_files()
        
        tasks = [self.async_read_tribe_file(tf) for tf in tribe_files]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        tribes = []
        for result in results:
            if isinstance(result, TribeData):
                tribes.append(result)
        
        return tribes
    
    async def async_read_player_inventory(self, profile_path: Path) -> List[Dict]:
        """
        Read player inventory async.
        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            read_inventory_from_profile,
            profile_path
        )


async def async_scan_all_servers(cluster_root: Path) -> Dict[str, AsyncArkSaveReader]:
    """
    Async scan of all servers in cluster.
    
    Args:
        cluster_root: Path to cluster root (e.g., R:/PhoenixArk)
    
    Returns:
        Dict mapping server name to AsyncArkSaveReader
    """
    if not HAS_AIOFILES:
        raise ImportError("aiofiles required for async operations")
    
    readers = {}
    
    # Directory scanning is fast, do it sync
    for server_dir in cluster_root.glob('asaserver_*'):
        if not server_dir.is_dir():
            continue
        
        saved_arks_dir = server_dir / 'ShooterGame' / 'Saved' / 'SavedArks'
        if not saved_arks_dir.exists():
            continue
        
        for map_dir in saved_arks_dir.iterdir():
            if map_dir.is_dir():
                reader = AsyncArkSaveReader(map_dir)
                if reader.is_valid():
                    server_name = server_dir.name.replace('asaserver_', '')
                    readers[server_name] = reader
                break
    
    return readers