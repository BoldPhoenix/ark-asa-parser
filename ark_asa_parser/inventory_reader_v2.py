"""
Enhanced inventory parsing for ARK ASA save files.

Parses full StructProperty arrays for inventory items with:
- Item blueprint/class names
- Quality/rating
- Durability
- Custom names
- Stack quantities
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional
import struct

from .simple_property_reader import read_ue_string_at


@dataclass
class ItemData:
    """Detailed item data from inventory"""
    item_name: str
    item_class: Optional[str] = None
    quantity: int = 1
    durability: Optional[float] = None
    quality: Optional[int] = None
    custom_name: Optional[str] = None
    is_blueprint: bool = False
    is_engram: bool = False


def _read_ue_string(data: bytes, pos: int) -> tuple[str, int]:
    """Read UE string and return (string, bytes_consumed)"""
    if pos + 4 > len(data):
        return ("", 0)
    
    length = struct.unpack('<i', data[pos:pos+4])[0]
    pos += 4
    
    if length == 0:
        return ("", 4)
    
    if length < 0:
        # UTF-16
        actual_len = (-length) * 2
        if pos + actual_len > len(data):
            return ("", 4)
        text = data[pos:pos+actual_len-2].decode('utf-16-le', errors='ignore')
        return (text, 4 + actual_len)
    else:
        # ASCII/UTF-8
        if pos + length > len(data):
            return ("", 4)
        text = data[pos:pos+length-1].decode('utf-8', errors='ignore')
        return (text, 4 + length)


def _parse_item_struct(data: bytes, start_pos: int) -> Optional[ItemData]:
    """
    Parse a single item struct from inventory array.
    This is a best-effort parser for common item properties.
    """
    item = ItemData(item_name="")
    pos = start_pos
    
    # Read properties until "None" terminator
    while pos < len(data) - 20:
        prop_name, name_bytes = _read_ue_string(data, pos)
        if not prop_name or prop_name == "None":
            break
        pos += name_bytes
        
        # Read property type
        prop_type, type_bytes = _read_ue_string(data, pos)
        if not prop_type:
            break
        pos += type_bytes
        
        # Read size (int64) and array index (int32)
        if pos + 12 > len(data):
            break
        prop_size = struct.unpack('<Q', data[pos:pos+8])[0]
        array_idx = struct.unpack('<i', data[pos+8:pos+12])[0]
        pos += 12
        
        # Parse value based on type
        if prop_type == "StrProperty":
            # String value has additional null byte before string
            if pos + 1 <= len(data):
                pos += 1
                value, val_bytes = _read_ue_string(data, pos)
                pos += val_bytes
                
                # Map to ItemData fields
                if prop_name in ("ItemName", "ItemArchetype", "ItemClass"):
                    if not item.item_name:
                        item.item_name = value
                    item.item_class = value
                elif prop_name == "CustomItemName":
                    item.custom_name = value
                    if not item.item_name:
                        item.item_name = value
        
        elif prop_type in ("IntProperty", "UInt32Property"):
            if pos + 5 <= len(data):
                pos += 1  # Null byte
                value = struct.unpack('<I', data[pos:pos+4])[0]
                pos += 4
                
                if prop_name == "ItemQuantity":
                    item.quantity = value
                elif prop_name in ("ItemRating", "ItemQualityIndex"):
                    item.quality = value
        
        elif prop_type in ("FloatProperty", "DoubleProperty"):
            val_size = 4 if prop_type == "FloatProperty" else 8
            if pos + val_size + 1 <= len(data):
                pos += 1
                if prop_type == "FloatProperty":
                    value = struct.unpack('<f', data[pos:pos+4])[0]
                else:
                    value = struct.unpack('<d', data[pos:pos+8])[0]
                pos += val_size
                
                if prop_name in ("ItemDurability", "Durability"):
                    item.durability = value
        
        elif prop_type == "BoolProperty":
            if pos + 2 <= len(data):
                value = data[pos] != 0
                pos += 2
                
                if prop_name == "bIsBlueprint":
                    item.is_blueprint = value
                elif prop_name == "bIsEngram":
                    item.is_engram = value
        
        else:
            # Skip unknown property type
            if pos + prop_size <= len(data):
                pos += prop_size
            else:
                break
    
    if item.item_name:
        return item
    return None


def read_inventory_from_profile(profile_path: Path) -> List[ItemData]:
    """
    Parse inventory from .arkprofile using struct array parsing.
    Falls back to heuristic if struct parsing fails.
    """
    data = Path(profile_path).read_bytes()
    items: List[ItemData] = []
    
    # Look for inventory ArrayProperty
    # Common names: "InventoryItems", "MyInventoryComponent", "ArkInventoryData"
    search_arrays = [b"InventoryItems", b"MyInventoryComponent", b"ArkInventoryData"]
    
    for array_name in search_arrays:
        pos = data.find(array_name)
        if pos == -1:
            continue
        
        # Find ArrayProperty marker after name
        array_prop_pos = data.find(b"ArrayProperty", pos)
        if array_prop_pos == -1 or array_prop_pos - pos > 100:
            continue
        
        # Jump past ArrayProperty marker and metadata
        # Format: property name, "ArrayProperty", size(8), array_idx(4), inner_type_name, element_count(4)
        scan_pos = array_prop_pos + len(b"ArrayProperty") + 1
        
        # Read size
        if scan_pos + 12 > len(data):
            continue
        size = struct.unpack('<Q', data[scan_pos:scan_pos+8])[0]
        scan_pos += 12  # skip size + array index
        
        # Read inner type (should be "StructProperty" for item arrays)
        inner_type, type_bytes = _read_ue_string(data, scan_pos)
        if inner_type != "StructProperty":
            continue
        scan_pos += type_bytes
        
        # Read element count
        if scan_pos + 4 > len(data):
            continue
        elem_count = struct.unpack('<i', data[scan_pos:scan_pos+4])[0]
        scan_pos += 4
        
        if elem_count <= 0 or elem_count > 1000:
            continue
        
        # Parse each struct
        for i in range(elem_count):
            item = _parse_item_struct(data, scan_pos)
            if item:
                items.append(item)
            # Move forward (heuristic: average struct ~200 bytes)
            scan_pos += 200
            if scan_pos >= len(data):
                break
        
        if items:
            break
    
    # Fallback: use heuristic name/quantity pairing if no structs found
    if not items:
        items = _heuristic_inventory_parse(data)
    
    return items


def _heuristic_inventory_parse(data: bytes) -> List[ItemData]:
    """Fallback heuristic parsing (original approach)"""
    custom_names = _find_all_string_values(data, "CustomItemName")
    base_names = _find_all_string_values(data, "ItemName")
    names = custom_names if custom_names else base_names
    quantities = _find_all_int_values(data, "ItemQuantity")
    
    count = min(len(names), len(quantities))
    items: List[ItemData] = []
    for i in range(count):
        name = names[i].strip()
        qty = int(quantities[i])
        if name:
            items.append(ItemData(item_name=name, quantity=qty))
    return items


def _find_all_string_values(data: bytes, prop_name: str, limit: int = 1000) -> List[str]:
    """Find all string property values by name"""
    values: List[str] = []
    search_bytes = prop_name.encode('ascii')
    pos = 0
    while len(values) < limit:
        pos = data.find(search_bytes, pos)
        if pos == -1:
            break
        if pos >= 4:
            length = struct.unpack('<i', data[pos-4:pos])[0]
            if length == len(prop_name) + 1:
                type_start = pos + len(search_bytes) + 1
                prop_type, type_bytes = read_ue_string_at(data, type_start)
                if prop_type == "StrProperty":
                    value_pos = type_start + type_bytes + 8 + 1
                    if value_pos <= len(data):
                        value, _ = read_ue_string_at(data, value_pos)
                        if value:
                            values.append(value)
        pos += 1
    return values


def _find_all_int_values(data: bytes, prop_name: str, limit: int = 1000) -> List[int]:
    """Find all int property values by name"""
    values: List[int] = []
    search_bytes = prop_name.encode('ascii')
    pos = 0
    while len(values) < limit:
        pos = data.find(search_bytes, pos)
        if pos == -1:
            break
        if pos >= 4:
            length = struct.unpack('<i', data[pos-4:pos])[0]
            if length == len(prop_name) + 1:
                type_start = pos + len(search_bytes) + 1
                prop_type, type_bytes = read_ue_string_at(data, type_start)
                if prop_type in ("IntProperty", "UInt32Property"):
                    value_pos = type_start + type_bytes + 8 + 1
                    if value_pos + 4 <= len(data):
                        values.append(struct.unpack('<I', data[value_pos:value_pos+4])[0])
        pos += 1
    return values