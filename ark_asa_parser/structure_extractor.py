"""
Structure (building) data extraction from world save files.

Parses the world .ark SQLite database to extract structure information
including type, health, owner, tribe, and location.
"""
import sqlite3
import struct
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class StructureData:
    """Represents a placed structure/building"""
    actor_id: str
    structure_type: str
    structure_name: Optional[str] = None  # Custom name if any
    health: float = 0
    max_health: float = 0
    owner_name: Optional[str] = None
    tribe_id: Optional[int] = None
    tribe_name: Optional[str] = None
    location_x: float = 0
    location_y: float = 0
    location_z: float = 0
    is_locked: bool = False


class StructureExtractor:
    """Extract structure data from ARK world saves"""
    
    # Common structure class patterns
    STRUCTURE_PATTERNS = [
        b'_C',
        b'Structure_',
        b'StorageBox_',
        b'Bed_',
        b'Door_',
        b'Wall_',
        b'Foundation_',
        b'Ceiling_',
        b'Ramp_',
        b'Pillar_',
        b'Fence_',
        b'Gate_',
    ]
    
    # Structure categories for classification
    STRUCTURE_CATEGORIES = {
        'StorageBox': 'Storage',
        'Vault': 'Storage',
        'Refrigerator': 'Storage',
        'Preserving': 'Storage',
        
        'Bed': 'Spawn Point',
        'SleepingBag': 'Spawn Point',
        
        'Foundation': 'Building',
        'Wall': 'Building',
        'Ceiling': 'Building',
        'Door': 'Building',
        'Doorframe': 'Building',
        'Window': 'Building',
        'Ramp': 'Building',
        'Pillar': 'Building',
        'Stair': 'Building',
        
        'Fence': 'Defense',
        'Gate': 'Defense',
        'Turret': 'Defense',
        'PlantSpecies': 'Defense',
        
        'Forge': 'Crafting',
        'Smithy': 'Crafting',
        'Fabricator': 'Crafting',
        'ChemBench': 'Crafting',
        'Mortar': 'Crafting',
        'CookingPot': 'Crafting',
        'Grill': 'Crafting',
        
        'Generator': 'Utility',
        'AirConditioner': 'Utility',
        'Transmitter': 'Utility',
        'TekGenerator': 'Utility',
    }
    
    @staticmethod
    def _read_string_at_offset(data: bytes, offset: int) -> Optional[str]:
        """Read length-prefixed string from binary data"""
        try:
            if offset + 4 > len(data):
                return None
            
            length = struct.unpack('<i', data[offset:offset+4])[0]
            
            if length < 0 or length > 10000:
                return None
            
            if offset + 4 + length > len(data):
                return None
            
            string_data = data[offset+4:offset+4+length]
            
            try:
                return string_data.decode('utf-8').rstrip('\x00')
            except:
                try:
                    return string_data.decode('ascii', errors='ignore').rstrip('\x00')
                except:
                    return None
        except:
            return None
    
    @staticmethod
    def _extract_type_from_class(class_name: str) -> str:
        """Extract structure type from class identifier"""
        # Example: "StorageBox_Large_C" -> "Storage Box Large"
        # Example: "Wall_Stone_C" -> "Wall Stone"
        
        # Remove common suffixes
        clean = class_name.replace('_C', '').replace('_BP', '')
        
        # Split by underscores and filter
        parts = [p for p in clean.split('_') if p and p not in ['Structure', 'PrimalItem']]
        
        return ' '.join(parts) if parts else class_name
    
    @classmethod
    def _categorize_structure(cls, structure_type: str) -> str:
        """Categorize structure by type"""
        for keyword, category in cls.STRUCTURE_CATEGORIES.items():
            if keyword.lower() in structure_type.lower():
                return category
        return 'Other'
    
    @classmethod
    def _parse_actor_data(cls, actor_data: bytes) -> Optional[StructureData]:
        """Parse binary actor data to extract structure information"""
        try:
            structure = StructureData(
                actor_id="",
                structure_type="Unknown"
            )
            
            # Search for class name patterns
            for pattern in cls.STRUCTURE_PATTERNS:
                pos = actor_data.find(pattern)
                if pos != -1:
                    # Look backward for class name
                    search_start = max(0, pos - 200)
                    for i in range(pos - 10, search_start, -1):
                        class_name = cls._read_string_at_offset(actor_data, i)
                        if class_name and len(class_name) > 3:
                            structure.structure_type = cls._extract_type_from_class(class_name)
                            break
                    break
            
            # Search for common properties
            prop_searches = {
                b'OwnerName': 'owner_name',
                b'TribeName': 'tribe_name',
                b'bIsLocked': 'is_locked',
                b'CustomName': 'structure_name',
            }
            
            for prop_bytes, prop_name in prop_searches.items():
                pos = actor_data.find(prop_bytes)
                if pos != -1:
                    search_start = pos + len(prop_bytes)
                    search_end = min(search_start + 100, len(actor_data))
                    
                    if prop_name in ['owner_name', 'tribe_name', 'structure_name']:
                        for offset in range(search_start, search_end, 1):
                            value = cls._read_string_at_offset(actor_data, offset)
                            if value and len(value) > 0:
                                setattr(structure, prop_name, value)
                                break
                    
                    elif prop_name == 'is_locked':
                        for offset in range(search_start, search_end, 1):
                            if actor_data[offset:offset+1] in [b'\x00', b'\x01']:
                                structure.is_locked = (actor_data[offset] == 1)
                                break
            
            # Search for health values
            health_pos = actor_data.find(b'Health')
            if health_pos != -1:
                search_start = health_pos + 6
                search_end = min(search_start + 50, len(actor_data))
                for offset in range(search_start, search_end - 4, 1):
                    try:
                        value = struct.unpack('<f', actor_data[offset:offset+4])[0]
                        if 0 < value < 1000000:
                            structure.health = value
                            break
                    except:
                        continue
            
            # Search for tribe ID
            tribe_pos = actor_data.find(b'TargetingTeam')
            if tribe_pos != -1:
                search_start = tribe_pos + 13
                search_end = min(search_start + 50, len(actor_data))
                for offset in range(search_start, search_end - 4, 1):
                    try:
                        value = struct.unpack('<i', actor_data[offset:offset+4])[0]
                        if value > 0:
                            structure.tribe_id = value
                            break
                    except:
                        continue
            
            # Only return if we found meaningful data
            if structure.structure_type != "Unknown" or structure.tribe_name or structure.owner_name:
                return structure
            
            return None
            
        except Exception:
            return None
    
    @classmethod
    def extract_structures_from_world(cls, world_ark_path: Path) -> List[StructureData]:
        """
        Extract all structures from world save file.
        
        Args:
            world_ark_path: Path to the .ark world save file (SQLite database)
        
        Returns:
            List of StructureData objects
        """
        structures = []
        
        if not world_ark_path.exists():
            return structures
        
        try:
            conn = sqlite3.connect(world_ark_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT key, value FROM game")
            
            for row in cursor.fetchall():
                key = row[0]
                value = row[1]
                
                if not value:
                    continue
                
                # Check if this looks like a structure actor
                # Skip if it's clearly a dino or player
                if b'Character' in value or b'Player' in value:
                    continue
                
                # Look for structure indicators
                has_structure_marker = False
                for pattern in cls.STRUCTURE_PATTERNS:
                    if pattern in value:
                        has_structure_marker = True
                        break
                
                if not has_structure_marker:
                    continue
                
                structure = cls._parse_actor_data(value)
                if structure:
                    structure.actor_id = str(key) if key else ""
                    structures.append(structure)
            
            conn.close()
            
        except Exception as e:
            print(f"Error extracting structures from {world_ark_path}: {e}")
        
        return structures
    
    @classmethod
    def get_tribe_structures(cls, world_ark_path: Path, tribe_id: int) -> List[StructureData]:
        """Get all structures belonging to a specific tribe"""
        all_structures = cls.extract_structures_from_world(world_ark_path)
        return [s for s in all_structures if s.tribe_id == tribe_id]
    
    @classmethod
    def get_structure_summary(cls, world_ark_path: Path) -> Dict[str, Dict[str, int]]:
        """
        Get summary of structures by category and type.
        
        Returns:
            Dict with categories and counts
        """
        structures = cls.extract_structures_from_world(world_ark_path)
        
        by_category = {}
        by_type = {}
        
        for structure in structures:
            category = cls._categorize_structure(structure.structure_type)
            by_category[category] = by_category.get(category, 0) + 1
            
            struct_type = structure.structure_type
            by_type[struct_type] = by_type.get(struct_type, 0) + 1
        
        return {
            'by_category': dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True)),
            'by_type': dict(sorted(by_type.items(), key=lambda x: x[1], reverse=True)[:20]),  # Top 20
            'total': len(structures)
        }
    
    @classmethod
    def search_structures(cls, world_ark_path: Path, search_term: str) -> List[StructureData]:
        """Search for structures by type or owner"""
        all_structures = cls.extract_structures_from_world(world_ark_path)
        search_lower = search_term.lower()
        
        results = []
        for structure in all_structures:
            if search_lower in structure.structure_type.lower():
                results.append(structure)
            elif structure.owner_name and search_lower in structure.owner_name.lower():
                results.append(structure)
            elif structure.tribe_name and search_lower in structure.tribe_name.lower():
                results.append(structure)
        
        return results