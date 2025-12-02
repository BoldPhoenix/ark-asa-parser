"""
Extract ALL players from ALL servers to build the most accurate XP table possible.
"""

from pathlib import Path
from ark_asa_parser import scan_all_servers

cluster_root = Path(r"R:\PhoenixArk")

print("Scanning all servers for player data...")
print("="*70)

servers = scan_all_servers(cluster_root)

all_player_data = []

for server_name, reader in servers.items():
    players = reader.get_all_players()
    print(f"{server_name:15s}: {len(players):3d} players")
    
    for p in players:
        if hasattr(p, 'experience') and hasattr(p, 'level'):
            xp = p.experience
            level = p.level
            name = p.character_name if hasattr(p, 'character_name') else "Unknown"
            
            # Only include players with meaningful XP (skip level 1 with 0-100 XP)
            if xp > 500:
                all_player_data.append((level, xp, name, server_name))

print(f"\nTotal players with XP data: {len(all_player_data)}")

# Group by level to find consensus XP values
from collections import defaultdict
level_xp_data = defaultdict(list)

for level, xp, name, server in all_player_data:
    if level > 0:  # Skip invalid levels
        level_xp_data[level].append(xp)

print(f"\nLevel distribution:")
print("-"*70)

# Show how many players we have at each level range
level_ranges = [(1, 20), (21, 50), (51, 80), (81, 110), (111, 140), (141, 180)]
for low, high in level_ranges:
    count = sum(1 for lvl in level_xp_data.keys() if low <= lvl <= high)
    total_players = sum(len(level_xp_data[lvl]) for lvl in level_xp_data.keys() if low <= lvl <= high)
    if count > 0:
        print(f"  Levels {low:3d}-{high:3d}: {count:3d} unique levels, {total_players:4d} total players")

# Find median XP for each level (more robust than mean)
print(f"\nMedian XP by level (sample):")
print("-"*70)

level_medians = {}
for level in sorted(level_xp_data.keys()):
    xp_values = sorted(level_xp_data[level])
    median_xp = xp_values[len(xp_values) // 2]
    level_medians[level] = median_xp
    
    if level % 10 == 0 or level > 130:
        player_count = len(xp_values)
        xp_range = f"{min(xp_values):,} - {max(xp_values):,}"
        print(f"  Level {level:3d}: {median_xp:>12,} XP (n={player_count:3d}, range: {xp_range})")

# Save detailed data
with open("all_server_player_data.txt", "w", encoding="utf-8") as f:
    f.write(f"# Complete player data from all servers\n")
    f.write(f"# Total: {len(all_player_data)} players\n\n")
    f.write("# Level -> Median XP\n")
    f.write("level_median_xp = {\n")
    for level in sorted(level_medians.keys()):
        f.write(f"    {level}: {level_medians[level]},\n")
    f.write("}\n")

print(f"\nData saved to: all_server_player_data.txt")
print(f"\nWe have XP data for {len(level_medians)} unique levels!")
