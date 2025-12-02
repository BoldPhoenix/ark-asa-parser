"""List all players on Astraeos server to find the right IDs"""

from pathlib import Path
from ark_asa_parser import scan_all_servers

cluster_root = Path(r"R:\PhoenixArk")

print("Scanning servers...\n")

servers = scan_all_servers(cluster_root)

for server_name, reader in servers.items():
    print(f"\n=== {server_name} ===")
    
    all_players = reader.get_all_players()
    
    print(f"Found {len(all_players)} players:\n")
    
    for p in all_players:
        player_id = p.player_id if hasattr(p, 'player_id') else "unknown"
        char_name = p.character_name if hasattr(p, 'character_name') else "unknown"
        xp = p.experience if hasattr(p, 'experience') else 0
        level = p.level if hasattr(p, 'level') else 0
        
        print(f"  {char_name:20s} | ID: {player_id:12s} | Level: {level:3d} | XP: {xp:>12,.0f}")
