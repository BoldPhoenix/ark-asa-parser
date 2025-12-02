"""
Inventory parsing prototype for ARK ASA .arkprofile files.

This prototype uses a heuristic approach based on repeated property name
occurrences to extract item names and quantities. It is not a full UE5
struct parser, but provides useful data for bots and tooling.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import List

from .simple_property_reader import (
    read_ue_string_at,
)

import struct


@dataclass
class ItemData:
    item_name: str
    quantity: int


def _find_all_string_values(data: bytes, prop_name: str, limit: int = 1000) -> List[str]:
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


def read_inventory_from_profile(profile_path: Path) -> List[ItemData]:
    """
    Heuristic inventory extraction:
    - Collect all occurrences of "ItemName" (strings)
    - Collect all occurrences of "ItemQuantity" (ints)
    - Zip them in order to produce ItemData entries
    This is a best-effort prototype and may not perfectly align names/quantities for all items.
    """
    data = Path(profile_path).read_bytes()

    # Prefer CustomItemName when present, fallback to ItemName
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
