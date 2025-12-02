"""
XP to Level mapping utilities for ARK: Survival Ascended.

This module provides a pluggable mechanism to map experience points (XP)
to character level. ASA's exact XP progression table can vary by server
configuration. To avoid hardcoding incorrect values, callers can provide
an XP threshold table. If no table is provided, xp_to_level returns None.

Usage:
    from ark_asa_parser.levels import xp_to_level

    # Provide an XP threshold table such that table[level] is minimum XP
    # required for that level (1-indexed or 0-indexed supported).
    ASA_DEFAULT_XP_TABLE = [0, 5, 15, 30, 50, ...]  # Example placeholder

    level = xp_to_level(xp, xp_table=ASA_DEFAULT_XP_TABLE)
"""

from bisect import bisect_right
from typing import List, Optional


def xp_to_level(xp: float, xp_table: Optional[List[float]] = None, one_indexed: bool = True) -> Optional[int]:
    """
    Convert experience points to level using a provided XP threshold table.

    Args:
        xp: Experience points value.
        xp_table: A list where each element is the minimum XP required for a given level.
                  If one_indexed=True, xp_table[0] should be the XP required for level 1.
                  If one_indexed=False, xp_table[0] is level 0 (not typical for ASA).
        one_indexed: Whether the provided table is one-indexed (default True).

    Returns:
        The computed level (int) or None if no table provided.
    """
    if xp_table is None or len(xp_table) == 0:
        return None

    # Normalize to an ascending table
    table = list(xp_table)

    # Find the rightmost position to insert xp to keep order
    idx = bisect_right(table, xp)

    if one_indexed:
        # idx corresponds directly to the level number when one-indexed
        level = max(1, min(idx, len(table)))
    else:
        # Convert zero-indexed levels to human levels by adding 1
        level = max(1, min(idx + 1, len(table)))

    return level
