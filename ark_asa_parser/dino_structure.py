"""
Basic Dino and Structure data stubs for ARK ASA parsing.

These provide simple dataclasses and lightweight count extraction where
available. Full object enumeration requires deeper UE5 struct parsing of
the world save and is left as future work.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .simple_property_reader import find_int_property


@dataclass
class DinoData:
    tribe_id: Optional[int]
    class_name: str = ""
    name: str = ""


@dataclass
class StructureData:
    tribe_id: Optional[int]
    class_name: str = ""
    name: str = ""


def try_get_tribe_dino_count(tribe_file: Path) -> Optional[int]:
    """Best-effort: read a tamed dino count from a tribe file if present."""
    try:
        data = Path(tribe_file).read_bytes()
        # Common property names seen in tribe files
        for key in ("TamedDinoCount", "tamed_dino_count"):
            val = find_int_property(data, key)
            if isinstance(val, int):
                return val
    except Exception:
        return None
    return None
