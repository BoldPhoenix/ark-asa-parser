"""
Dino (tamed creature) data extraction from world save files.

Parses the world .ark SQLite database to extract tamed dino information
including species, level, stats, owner, and location.
"""
import sqlite3
import struct
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class DinoData:
    """Represents a tamed dinosaur/creature"""
    actor_id: str
    species_name: str
    dino_name: Optional[str] = None  # Custom name
    level: int = 0
    base_level: int = 0
    experience: float = 0
    owner_name: Optional[str] = None
    tribe_id: Optional[int] = None
    health: float = 0
    stamina: float = 0
    torpor: float = 0
    oxygen: float = 0
    food: float = 0
    weight: float = 0
    melee: float = 100.0
    speed: float = 100.0
    is_baby: bool = False
    is_female: bool = False
    location_x: float = 0
    location_y: float = 0
    location_z: float = 0


class DinoExtractor:
    """Extract tamed dino data from ARK world saves"""
    
    # Common dino class name patterns
    DINO_CLASS_PATTERNS = [
        b'_Character_BP_C',
        b'_Character_C',
        b'Dino_Character_BP_C',
        b'_Dino_Character_C',
    ]
    
    # Properties to search for in actor data
    DINO_PROPERTIES = {
        b'TamedName': 'dino_name',
        b'CustomTag': 'dino_name',
        b'DinoNameTag': 'dino_name',
        
        b'bIsFemale': 'is_female',
        b'bIsBaby': 'is_baby',
        
        b'BaseCharacterLevel': 'base_level',
        b'CharacterLevel': 'level',
        b'ExtraCharacterLevel': 'level',
        
        b'TamerString': 'owner_name',
        b'OwnerName': 'owner_name',
        
        b'TargetingTeam': 'tribe_id',
        b'TribeName': 'tribe_name',
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
            
            # Try UTF-8 first
            try:
                return string_data.decode('utf-8').rstrip('\x00')
            except:
                # Try ASCII
                try:
                    return string_data.decode('ascii', errors='ignore').rstrip('\x00')
                except:
                    return None
        except:
            return None
    
    @staticmethod
    def _extract_species_from_class(class_name: str) -> str:
        """Extract species name from class identifier"""
        # Example: "Raptor_Character_BP_C" -> "Raptor"
        # Example: "MegaRex_Character_BP_C" -> "MegaRex"
        
        parts = class_name.replace('_Character_BP_C', '').replace('_Character_C', '').split('_')
        
        # Remove common prefixes
        if parts and parts[0] in ['Dino', 'Character', 'BP']:
            parts = parts[1:]
        
        return ' '.join(parts) if parts else class_name
    
    @classmethod
    def _parse_actor_data(cls, actor_data: bytes) -> Optional[DinoData]:
        """Parse binary actor data to extract dino information"""
        try:
            dino = DinoData(
                actor_id="",
                species_name="Unknown"
            )
            
            # Search for class name to determine species
            for pattern in cls.DINO_CLASS_PATTERNS:
                pos = actor_data.find(pattern)
                if pos != -1:
                    # Look backward for class name string
                    search_start = max(0, pos - 200)
                    for i in range(pos - 10, search_start, -1):
                        class_name = cls._read_string_at_offset(actor_data, i)
                        if class_name and pattern.decode('ascii', errors='ignore') in class_name:
                            dino.species_name = cls._extract_species_from_class(class_name)
                            break
                    break
            
            # Search for properties
            for prop_bytes, prop_name in cls.DINO_PROPERTIES.items():
                pos = actor_data.find(prop_bytes)
                if pos != -1:
                    # Try to read value after property name
                    search_start = pos + len(prop_bytes)
                    search_end = min(search_start + 100, len(actor_data))
                    
                    if prop_name in ['dino_name', 'owner_name', 'tribe_name']:
                        # String property
                        for offset in range(search_start, search_end, 1):
                            value = cls._read_string_at_offset(actor_data, offset)
                            if value and len(value) > 0:
                                setattr(dino, prop_name, value)
                                break
                    
                    elif prop_name in ['level', 'base_level']:
                        # Integer property
                        for offset in range(search_start, search_end - 4, 1):
                            try:
                                value = struct.unpack('<i', actor_data[offset:offset+4])[0]
                                if 0 < value < 1000:  # Sanity check
                                    setattr(dino, prop_name, value)
                                    break
                            except:
                                continue
                    
                    elif prop_name == 'tribe_id':
                        # Integer property
                        for offset in range(search_start, search_end - 4, 1):
                            try:
                                value = struct.unpack('<i', actor_data[offset:offset+4])[0]
                                if value > 0:
                                    dino.tribe_id = value
                                    break
                            except:
                                continue
                    
                    elif prop_name in ['is_female', 'is_baby']:
                        # Boolean property (look for 0x00 or 0x01)
                        for offset in range(search_start, search_end, 1):
                            if actor_data[offset:offset+1] in [b'\x00', b'\x01']:
                                setattr(dino, prop_name, actor_data[offset] == 1)
                                break
            
            # Only return if we found meaningful data
            if dino.species_name != "Unknown" or dino.dino_name or dino.owner_name:
                return dino
            
            return None
            
        except Exception as e:
            return None
    
    @classmethod
    def extract_dinos_from_world(cls, world_ark_path: Path) -> List[DinoData]:
        """
        Extract all tamed dinos from world save file.
        
        Args:
            world_ark_path: Path to the .ark world save file (SQLite database)
        
        Returns:
            List of DinoData objects for tamed creatures
        """
        dinos = []
        
        if not world_ark_path.exists():
            return dinos
        
        try:
            conn = sqlite3.connect(world_ark_path)
            cursor = conn.cursor()
            
            # Query the game table which contains actor data
            cursor.execute("SELECT key, value FROM game")
            
            for row in cursor.fetchall():
                key = row[0]
                value = row[1]
                
                if not value:
                    continue
                
                # Check if this looks like a dino actor
                # Tamed dinos typically have Character in their class name
                if b'Character' not in value and b'Dino' not in value:
                    continue
                
                # Skip wild dinos (look for taming indicators)
                if b'Tamed' not in value and b'Owner' not in value and b'Tribe' not in value:
                    continue
                
                dino = cls._parse_actor_data(value)
                if dino:
                    dino.actor_id = str(key) if key else ""
                    dinos.append(dino)
            
            conn.close()
            
        except Exception as e:
            print(f"Error extracting dinos from {world_ark_path}: {e}")
        
        return dinos
    
    @classmethod
    def get_tribe_dinos(cls, world_ark_path: Path, tribe_id: int) -> List[DinoData]:
        """Get all dinos belonging to a specific tribe"""
        all_dinos = cls.extract_dinos_from_world(world_ark_path)
        return [d for d in all_dinos if d.tribe_id == tribe_id]
    
    @classmethod
    def get_dino_summary(cls, world_ark_path: Path) -> Dict[str, int]:
        """
        Get summary of dinos by species.
        
        Returns:
            Dict mapping species name to count
        """
        dinos = cls.extract_dinos_from_world(world_ark_path)
        
        summary = {}
        for dino in dinos:
            species = dino.species_name
            summary[species] = summary.get(species, 0) + 1
        
        return dict(sorted(summary.items(), key=lambda x: x[1], reverse=True))
    
    @classmethod
    def search_dinos_by_name(cls, world_ark_path: Path, search_term: str) -> List[DinoData]:
        """Search for dinos by custom name or species"""
        all_dinos = cls.extract_dinos_from_world(world_ark_path)
        search_lower = search_term.lower()
        
        results = []
        for dino in all_dinos:
            if dino.dino_name and search_lower in dino.dino_name.lower():
                results.append(dino)
            elif search_lower in dino.species_name.lower():
                results.append(dino)
        
        return results