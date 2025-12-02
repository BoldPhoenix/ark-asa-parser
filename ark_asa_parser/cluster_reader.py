"""
Cluster transfer data reader for ARK: Survival Ascended.

Parses the ClusterObjects folder to extract transferred characters,
items, and dinosaurs between servers in a cluster.
"""
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import struct


@dataclass
class ClusterTransfer:
    """Represents a transferred item/character in cluster storage"""
    file_name: str
    file_path: Path
    file_size: int
    steam_id: Optional[str] = None
    character_name: Optional[str] = None
    upload_time: Optional[int] = None
    transfer_type: str = "unknown"  # 'character', 'item', 'dino'


def read_cluster_file(file_path: Path) -> Optional[ClusterTransfer]:
    """
    Read a single cluster transfer file.
    
    ClusterObjects files use a similar binary format to profile/tribe files.
    
    Args:
        file_path: Path to .arkcharactersetting, .arkitem, etc.
    
    Returns:
        ClusterTransfer object or None if parsing fails
    """
    try:
        data = file_path.read_bytes()
        
        transfer = ClusterTransfer(
            file_name=file_path.name,
            file_path=file_path,
            file_size=len(data)
        )
        
        # Determine transfer type from extension
        suffix = file_path.suffix.lower()
        if 'character' in suffix:
            transfer.transfer_type = 'character'
        elif 'item' in suffix:
            transfer.transfer_type = 'item'
        elif 'dino' in suffix or 'creature' in suffix:
            transfer.transfer_type = 'dino'
        
        # Try to extract Steam ID from filename
        # Format often: SteamID_timestamp.arkcharactersetting
        parts = file_path.stem.split('_')
        if parts and parts[0].isdigit() and len(parts[0]) == 17:
            transfer.steam_id = parts[0]
        
        # Search for common properties
        if b'CharacterName' in data:
            pos = data.find(b'CharacterName')
            # Try to read string after property name
            try:
                # Skip property name and type info
                offset = pos + len(b'CharacterName') + 20
                if offset < len(data):
                    # Look for null-terminated string
                    end = data.find(b'\x00', offset, offset + 200)
                    if end != -1:
                        name_data = data[offset:end]
                        # Filter to printable chars
                        name = ''.join(chr(b) for b in name_data if 32 <= b < 127)
                        if name:
                            transfer.character_name = name
            except:
                pass
        
        # Look for upload timestamp (often near start of file)
        # This is speculative - actual format may vary
        if len(data) >= 16:
            try:
                # Check first few integers for timestamp-like values
                for offset in [4, 8, 12, 16, 20]:
                    if offset + 4 <= len(data):
                        value = struct.unpack('<I', data[offset:offset+4])[0]
                        # Unix timestamp range check (2020-2030)
                        if 1577836800 < value < 1893456000:
                            transfer.upload_time = value
                            break
            except:
                pass
        
        return transfer
        
    except Exception as e:
        print(f"Error reading cluster file {file_path}: {e}")
        return None


def scan_cluster_folder(cluster_path: Path) -> Dict[str, List[ClusterTransfer]]:
    """
    Scan ClusterObjects folder and categorize transfers.
    
    Args:
        cluster_path: Path to ClusterObjects folder or parent SavedArks folder
    
    Returns:
        Dict with keys: 'characters', 'items', 'dinos', 'unknown'
    """
    # Handle both direct ClusterObjects path and parent SavedArks path
    if cluster_path.name == 'ClusterObjects':
        cluster_dir = cluster_path
    else:
        cluster_dir = cluster_path / 'ClusterObjects'
    
    if not cluster_dir.exists():
        return {
            'characters': [],
            'items': [],
            'dinos': [],
            'unknown': []
        }
    
    results: Dict[str, List[ClusterTransfer]] = {
        'characters': [],
        'items': [],
        'dinos': [],
        'unknown': []
    }
    
    # Scan all files in ClusterObjects
    for file_path in cluster_dir.iterdir():
        if file_path.is_file():
            transfer = read_cluster_file(file_path)
            if transfer:
                # Categorize by type
                if transfer.transfer_type == 'character':
                    results['characters'].append(transfer)
                elif transfer.transfer_type == 'item':
                    results['items'].append(transfer)
                elif transfer.transfer_type == 'dino':
                    results['dinos'].append(transfer)
                else:
                    results['unknown'].append(transfer)
    
    return results


def get_player_cluster_data(cluster_path: Path, steam_id: str) -> List[ClusterTransfer]:
    """
    Get all cluster transfers for a specific player.
    
    Args:
        cluster_path: Path to ClusterObjects folder
        steam_id: Steam ID to filter by
    
    Returns:
        List of ClusterTransfer objects for this player
    """
    all_transfers = scan_cluster_folder(cluster_path)
    
    player_transfers = []
    for category in all_transfers.values():
        for transfer in category:
            if transfer.steam_id == steam_id:
                player_transfers.append(transfer)
    
    return player_transfers


def get_cluster_summary(cluster_path: Path) -> Dict[str, any]:
    """
    Get summary statistics for cluster transfers.
    
    Returns:
        Dict with counts and sizes by category
    """
    transfers = scan_cluster_folder(cluster_path)
    
    summary = {
        'total_files': 0,
        'total_size_bytes': 0,
        'by_type': {}
    }
    
    for transfer_type, transfer_list in transfers.items():
        count = len(transfer_list)
        total_size = sum(t.file_size for t in transfer_list)
        
        summary['total_files'] += count
        summary['total_size_bytes'] += total_size
        
        summary['by_type'][transfer_type] = {
            'count': count,
            'size_bytes': total_size,
            'size_mb': round(total_size / (1024 * 1024), 2)
        }
    
    summary['total_size_mb'] = round(summary['total_size_bytes'] / (1024 * 1024), 2)
    
    # Count unique Steam IDs
    unique_steam_ids = set()
    for transfer_list in transfers.values():
        for transfer in transfer_list:
            if transfer.steam_id:
                unique_steam_ids.add(transfer.steam_id)
    
    summary['unique_players'] = len(unique_steam_ids)
    
    return summary