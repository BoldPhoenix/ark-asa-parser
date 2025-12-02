"""
Full player stats extraction (health, stamina, weight, etc.)

Parses FloatProperty and DoubleProperty values for character attributes.
"""
from pathlib import Path
from typing import Dict, Optional
import struct


class PlayerStatsReader:
    """Extract detailed player statistics from profile files"""
    
    # Common stat property names in ARK
    STAT_PROPERTIES = {
        'CharacterStatusComponent_Extra_CharacterLevel': 'level',
        'CharacterStatusComponent_ExtraCharacterLevel': 'level',
        'MyCharacterStatusComponent_ExtraCharacterLevel': 'level',
        
        'Health': 'health',
        'MaxHealth': 'max_health',
        'CurrentStatusValues': 'status_values',  # Array of floats
        
        'Stamina': 'stamina',
        'MaxStamina': 'max_stamina',
        
        'Torpor': 'torpor',
        'MaxTorpor': 'max_torpor',
        
        'Oxygen': 'oxygen',
        'MaxOxygen': 'max_oxygen',
        
        'Food': 'food',
        'MaxFood': 'max_food',
        
        'Water': 'water',
        'MaxWater': 'max_water',
        
        'Weight': 'weight',
        'MaxWeight': 'max_weight',
        
        'MeleeDamage': 'melee_damage',
        'MovementSpeed': 'movement_speed',
        'CraftingSpeed': 'crafting_speed',
        
        'Fortitude': 'fortitude',
    }
    
    @staticmethod
    def _read_float(data: bytes, offset: int) -> Optional[float]:
        """Read 4-byte float at offset"""
        try:
            if offset + 4 <= len(data):
                return struct.unpack('<f', data[offset:offset+4])[0]
        except:
            pass
        return None
    
    @staticmethod
    def _read_double(data: bytes, offset: int) -> Optional[float]:
        """Read 8-byte double at offset"""
        try:
            if offset + 8 <= len(data):
                return struct.unpack('<d', data[offset:offset+8])[0]
        except:
            pass
        return None
    
    @classmethod
    def read_player_stats(cls, profile_path: Path) -> Dict[str, float]:
        """
        Extract full player stats from profile file.
        
        Args:
            profile_path: Path to .arkprofile file
        
        Returns:
            Dict mapping stat name to value
        """
        try:
            data = profile_path.read_bytes()
        except Exception as e:
            print(f"Error reading profile: {e}")
            return {}
        
        stats = {}
        
        # Search for each stat property
        for prop_name, stat_name in cls.STAT_PROPERTIES.items():
            prop_bytes = prop_name.encode('utf-8')
            pos = data.find(prop_bytes)
            
            if pos != -1:
                # Try to read value after property name
                # Skip property name, type info (typically ~20-40 bytes)
                search_start = pos + len(prop_bytes)
                search_end = min(search_start + 100, len(data))
                
                # Look for FloatProperty or DoubleProperty marker
                if b'FloatProperty' in data[pos:search_end]:
                    # FloatProperty typically has value ~20-30 bytes after name
                    for offset in range(search_start, search_end - 4, 1):
                        value = cls._read_float(data, offset)
                        if value is not None and 0 <= value < 1000000:  # Sanity check
                            stats[stat_name] = value
                            break
                
                elif b'DoubleProperty' in data[pos:search_end]:
                    # DoubleProperty typically has value ~20-40 bytes after name
                    for offset in range(search_start, search_end - 8, 1):
                        value = cls._read_double(data, offset)
                        if value is not None and 0 <= value < 1000000:  # Sanity check
                            stats[stat_name] = value
                            break
        
        # Try to extract status values array (health, stamina, etc.)
        cls._extract_status_array(data, stats)
        
        return stats
    
    @classmethod
    def _extract_status_array(cls, data: bytes, stats: Dict):
        """
        Extract CurrentStatusValues array if present.
        
        ASA often stores current stat values in an array:
        [Health, Stamina, Oxygen, Food, Water, Weight, Melee, Speed, ...]
        """
        array_marker = b'CurrentStatusValues'
        pos = data.find(array_marker)
        
        if pos == -1:
            return
        
        # Try to find array count (Int32 typically appears before array data)
        search_start = pos + len(array_marker)
        search_end = min(search_start + 100, len(data))
        
        for offset in range(search_start, search_end - 4, 1):
            try:
                array_count = struct.unpack('<i', data[offset:offset+4])[0]
                
                # Sanity check: ASA typically has 8-12 status values
                if 5 < array_count < 20:
                    # Try to read array of floats starting after count
                    values = []
                    data_start = offset + 4
                    
                    for i in range(array_count):
                        val_offset = data_start + (i * 4)
                        value = cls._read_float(data, val_offset)
                        if value is not None:
                            values.append(value)
                    
                    # If we got reasonable values, map them to stats
                    if len(values) >= 8:
                        stat_names = ['health', 'stamina', 'torpor', 'oxygen', 
                                     'food', 'water', 'weight', 'melee_damage']
                        
                        for i, name in enumerate(stat_names):
                            if i < len(values) and values[i] > 0:
                                stats[f'current_{name}'] = values[i]
                        
                        break
            except:
                continue
    
    @classmethod
    def get_stat_summary(cls, profile_path: Path) -> Dict[str, any]:
        """
        Get human-readable stat summary.
        
        Returns:
            Dict with formatted stat information
        """
        stats = cls.read_player_stats(profile_path)
        
        summary = {
            'health': stats.get('current_health') or stats.get('health'),
            'stamina': stats.get('current_stamina') or stats.get('stamina'),
            'oxygen': stats.get('current_oxygen') or stats.get('oxygen'),
            'food': stats.get('current_food') or stats.get('food'),
            'water': stats.get('current_water') or stats.get('water'),
            'weight': stats.get('current_weight') or stats.get('weight'),
            'melee': stats.get('current_melee_damage') or stats.get('melee_damage'),
            'speed': stats.get('movement_speed'),
            'fortitude': stats.get('fortitude'),
            'crafting': stats.get('crafting_speed'),
            'level': stats.get('level'),
        }
        
        # Filter out None values
        return {k: v for k, v in summary.items() if v is not None}