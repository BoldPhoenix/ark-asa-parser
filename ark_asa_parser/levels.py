"""
XP to Level mapping utilities for ARK: Survival Ascended. 
"""
from bisect import bisect_right
from typing import List, Optional
import json
from pathlib import Path

from .xp_data import get_default_xp_table


def xp_to_level(xp: float, xp_table: Optional[List[float]] = None, one_indexed: bool = True) -> Optional[int]:
    """
    Convert experience points to level using an XP threshold table.
    
    Args:
        xp: Experience points value.
        xp_table: Optional XP threshold list. If None, uses bundled default ASA table.
        one_indexed: Whether the table is one-indexed (default True for ASA).
    
    Returns:
        The computed level (int) or None if xp_table empty.
    """
    if xp_table is None:
        xp_table = get_default_xp_table()
    
    if len(xp_table) == 0:
        return None

    table = list(xp_table)
    idx = bisect_right(table, xp)

    if one_indexed:
        level = max(1, min(idx, len(table)))
    else:
        level = max(1, min(idx + 1, len(table)))

    return level


def load_xp_table(json_path: str | Path) -> List[float]:
    """
    Load an XP threshold table from a JSON file.
    JSON should be a list/array of numbers (XP thresholds per level).
    """
    p = Path(json_path)
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("XP table JSON must be a list of numbers")
    return [float(x) for x in data]
