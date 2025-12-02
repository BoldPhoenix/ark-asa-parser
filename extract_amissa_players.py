"""
Extract XP from Amissa players to refine the curve.
"""

from pathlib import Path
from ark_asa_parser import scan_all_servers

# New players from Amissa screenshots
amissa_players = {
    "ShadiDK": 83,
    "Anjo": 89,
    "Lex XD": 89,
    "Axl": 143,  # High level - critical data point!
    "Tapeworm": 21,
    "Ami Fallen": 20,
    "Robf73": 74,
    "LadySif": 134,  # High level - critical!
    "Mathias": 96,
    "Eos": 39,
    "Sevey": 68,
    "Koco": 71,
}

cluster_root = Path(r"R:\PhoenixArk")

print("Extracting XP from Amissa players...")
print("="*70)

servers = scan_all_servers(cluster_root)

if "amissa" in servers:
    reader = servers["amissa"]
    all_players = reader.get_all_players()
    
    found_data = []
    
    for name, expected_level in amissa_players.items():
        for p in all_players:
            char_name = p.character_name if hasattr(p, 'character_name') else ""
            
            if char_name and char_name.lower() == name.lower():
                xp = p.experience if hasattr(p, 'experience') else 0
                
                found_data.append((expected_level, int(xp), char_name))
                print(f"{char_name:20s} | Level: {expected_level:3d} | XP: {xp:>12,.0f}")
                break
    
    print("\n" + "="*70)
    print(f"\nFound {len(found_data)} out of {len(amissa_players)} players")
    
    # Sort by level
    found_data.sort(key=lambda x: x[0])
    
    print("\nSorted by level:")
    print("-"*70)
    for level, xp, name in found_data:
        print(f"Level {level:3d}: {xp:>12,} XP  ({name})")
    
    # Save combined with previous data
    previous_data = [
        (9, 877, 'Rhyno'),
        (15, 1141, 'Tester'),
        (25, 3117, 'LionsLord'),
        (38, 7129, 'Mëlkor'),
        (64, 28091, 'Aatxe'),
        (71, 55484, 'Dc kid'),
        (78, 146580, 'Raven Yuri'),
        (82, 259671, 'Reina'),
        (88, 497641, 'Poli'),
        (90, 612400, 'Cassian'),
        (95, 975649, 'Sex4TRex'),
        (97, 1259269, 'Jake'),
        (114, 6179425, 'Joker'),
        (117, 7541021, 'Panther'),
        (131, 20947286, 'Jaxxx'),
        (132, 28614060, 'BoldPhoenix'),
    ]
    
    combined_data = previous_data + found_data
    combined_data.sort(key=lambda x: x[0])
    
    print("\n" + "="*70)
    print(f"\nCombined dataset: {len(combined_data)} players")
    print("-"*70)
    
    for level, xp, name in combined_data:
        if xp > 100:  # Skip very low XP
            print(f"Level {level:3d}: {xp:>12,} XP  ({name})")
    
    # Save to file
    with open("combined_player_data.txt", "w", encoding="utf-8") as f:
        f.write("# Combined player data from all servers\n")
        f.write("data_points = [\n")
        for level, xp, name in combined_data:
            if xp > 100:
                f.write(f"    ({level}, {xp}, '{name}'),\n")
        f.write("]\n")
    
    print("\nData saved to: combined_player_data.txt")

else:
    print("Amissa server not found!")
