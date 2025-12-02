"""
Search all servers for the Amissa screenshot players by name.
"""

from pathlib import Path
from ark_asa_parser import scan_all_servers

# Players from Amissa screenshots
target_names = ["ShadiDK", "Anjo", "Lex XD", "Axl", "Tapeworm", "Ami Fallen", 
                "Robf73", "LadySif", "Mathias", "Eos", "Sevey", "Koco"]

expected_levels = {
    "ShadiDK": 83, "Anjo": 89, "Lex XD": 89, "Axl": 143, "Tapeworm": 21,
    "Ami Fallen": 20, "Robf73": 74, "LadySif": 134, "Mathias": 96,
    "Eos": 39, "Sevey": 68, "Koco": 71,
}

cluster_root = Path(r"R:\PhoenixArk")
servers = scan_all_servers(cluster_root)

print("Searching all servers for Amissa screenshot players...")
print("="*70)

found_data = []

for server_name, reader in servers.items():
    all_players = reader.get_all_players()
    
    for p in all_players:
        char_name = p.character_name if hasattr(p, 'character_name') else ""
        
        if char_name in target_names:
            xp = p.experience if hasattr(p, 'experience') else 0
            expected_level = expected_levels.get(char_name, 0)
            
            found_data.append((expected_level, int(xp), char_name, server_name))
            print(f"{char_name:20s} | Level: {expected_level:3d} | XP: {xp:>12,.0f} | Server: {server_name}")

print("\n" + "="*70)
print(f"\nFound {len(found_data)} out of {len(target_names)} players")

if found_data:
    found_data.sort(key=lambda x: x[0])
    
    print("\nSorted by level:")
    print("-"*70)
    for level, xp, name, server in found_data:
        if xp > 100:
            print(f"Level {level:3d}: {xp:>12,} XP  ({name})")
