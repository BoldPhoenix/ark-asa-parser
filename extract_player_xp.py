"""
Extract experience values for specific players to determine exact XP curve.
"""

from pathlib import Path
from ark_asa_parser import ArkSaveReader

# Player data from screenshots
players = {
    "Sex4TRex": {"player_id": "774261199", "level": 95},
    "Melbar": {"player_id": "805919994", "level": 38},
    "Joker": {"player_id": "1089924149", "level": 114},
    "Cassian": {"player_id": "1492419039", "level": 90},
    "Panther": {"player_id": "1882790893", "level": 117},
}

# Known data point
players["BoldPhoenix"] = {"player_id": "unknown", "level": 132, "xp": 28615150}

astraeos_path = Path(r"R:\PhoenixArk\Astraeos")

print("Extracting experience values for players...\n")

reader = ArkSaveReader(astraeos_path)

for name, data in players.items():
    if "xp" in data:
        print(f"{name} (Level {data['level']}): {data['xp']:,} XP [Known]")
        continue
    
    # Find player in the save
    try:
        all_players = reader.get_all_players()
        
        # Find by player ID
        player_id = data["player_id"]
        found_player = None
        
        for p in all_players:
            if hasattr(p, 'player_id') and str(p.player_id) == player_id:
                found_player = p
                break
        
        if found_player and hasattr(found_player, 'experience'):
            xp = found_player.experience
            print(f"{name} (Level {data['level']}): {xp:,} XP")
            players[name]["xp"] = xp
        else:
            print(f"{name}: Player not found or no XP data")
    
    except Exception as e:
        print(f"{name}: Error - {e}")

print("\n" + "="*70)
print("\nData points for curve fitting:")
print("-" * 70)

# Sort by level
sorted_players = sorted(players.items(), key=lambda x: x[1]["level"])

for name, data in sorted_players:
    if "xp" in data:
        print(f"Level {data['level']:3d}: {data['xp']:>12,} XP  ({name})")

# Save to file for analysis
with open("player_xp_data.txt", "w", encoding="utf-8") as f:
    f.write("# Player XP Data Points\n")
    f.write("# Format: level, xp, player_name\n\n")
    f.write("data_points = [\n")
    for name, data in sorted_players:
        if "xp" in data:
            f.write(f"    ({data['level']}, {data['xp']}, '{name}'),\n")
    f.write("]\n")

print("\nData saved to: player_xp_data.txt")
