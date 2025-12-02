"""
Extract XP for all the new players from Island server.
"""

from pathlib import Path
from ark_asa_parser import scan_all_servers

# New players from Island screenshots
target_players = {
    "Tester": 15,
    "Raven Yuri": 78,  # Changed from just "Raven" to match actual name
    "Bundy": 105,
    "Jaxxx": 131,
    "The Govnaaa": 110,
    "Jake": 97,
    "May": 105,
    "Dc kid": 71,
    "Beyonx": 1,
    "Reina": 82,
    "Aatxe": 64,
    "oTomadorDeTerere": 1,
    "Poli": 88,
    "Ripstanlee": 83,
    "Rhyno": 9,
    "LionsLord": 25,
}

cluster_root = Path(r"R:\PhoenixArk")

print("Extracting XP from Island players...")
print("="*70)

servers = scan_all_servers(cluster_root)

if "island" in servers:
    reader = servers["island"]
    all_players = reader.get_all_players()
    
    found_data = []
    
    for name, expected_level in target_players.items():
        for p in all_players:
            char_name = p.character_name if hasattr(p, 'character_name') else ""
            
            # Match player name (case-insensitive)
            if char_name and char_name.lower() == name.lower():
                xp = p.experience if hasattr(p, 'experience') else 0
                level = p.level if hasattr(p, 'level') else 0
                
                found_data.append((expected_level, int(xp), char_name))
                print(f"{char_name:20s} | Expected Level: {expected_level:3d} | XP: {xp:>12,.0f}")
                break
    
    print("\n" + "="*70)
    print(f"\nFound {len(found_data)} out of {len(target_players)} players")
    
    # Combine with Astraeos data
    astraeos_data = [
        (38, 7_129, "Mëlkor"),
        (90, 612_400, "Cassian"),
        (95, 975_649, "Sex4TRex"),
        (114, 6_179_425, "Joker"),
        (117, 7_541_021, "Panther"),
        (132, 28_614_060, "BoldPhoenix"),
    ]
    
    print("\n" + "="*70)
    print("\nCombined data points (sorted by level):")
    print("-"*70)
    
    all_data = found_data + [(level, xp, name) for level, xp, name in astraeos_data]
    all_data.sort(key=lambda x: x[0])
    
    for level, xp, name in all_data:
        if xp > 0:  # Skip level 1 players with 0 XP
            print(f"Level {level:3d}: {xp:>12,} XP  ({name})")
    
    # Save to file for curve fitting
    with open("all_player_data.txt", "w", encoding="utf-8") as f:
        f.write("# All player data points\n")
        f.write("data_points = [\n")
        for level, xp, name in all_data:
            if xp > 0:
                f.write(f"    ({level}, {xp}, '{name}'),\n")
        f.write("]\n")
    
    print("\n" + "="*70)
    print("\nData saved to: all_player_data.txt")
    print(f"Total data points: {len([d for d in all_data if d[1] > 0])}")

else:
    print("Island server not found!")
