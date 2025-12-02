"""
Extract XP data for specific players from screenshots
Center and RagVegas maps from PhoenixArk cluster
"""

from pathlib import Path
from ark_asa_parser import ArkSaveReader

# Players from screenshots with their EOS IDs and levels
screenshot_players = {
    # Center map
    'WinterAngel': {'eos_id': '48D32991', 'level': 106, 'map': 'center'},
    'Mills': {'eos_id': '45928616', 'level': 109, 'map': 'center'},
    'Rexy The First': {'eos_id': '8A694030', 'level': 108, 'map': 'center'},
    'Coobiehoe': {'eos_id': '94535392', 'level': 108, 'map': 'center'},
    'Undertaker': {'eos_id': '807249848', 'level': 105, 'map': 'center'},
    'AJ': {'eos_id': '39941431I', 'level': 92, 'map': 'center'},
    'Humano': {'eos_id': '45023465', 'level': 6, 'map': 'center'},
    
    # RagVegas map
    'PiNk': {'eos_id': '617189832', 'level': 111, 'map': 'RagVegas'},
    'Tarzan': {'eos_id': '765408167', 'level': 136, 'map': 'RagVegas'},
    'hAcKeR': {'eos_id': '815596717', 'level': 91, 'map': 'RagVegas'},
    'PEPPERJACKCHEESE': {'eos_id': '88440822', 'level': 46, 'map': 'RagVegas'},
    'Jolly': {'eos_id': '453135554', 'level': 1, 'map': 'RagVegas'},
    'HelpMob': {'eos_id': '419292276', 'level': 3, 'map': 'RagVegas'},
    'Juice': {'eos_id': '327849583', 'level': 135, 'map': 'RagVegas'},
    'Xexu': {'eos_id': '179216803', 'level': 175, 'map': 'RagVegas'},
    'Weeheed': {'eos_id': '537460477', 'level': 77, 'map': 'RagVegas'},
    'Bella': {'eos_id': '858468751', 'level': 101, 'map': 'RagVegas'},
    'HHK': {'eos_id': '839916392', 'level': 29, 'map': 'RagVegas'},
    'Raven': {'eos_id': '785645934', 'level': 105, 'map': 'RagVegas'},
}

print("="*80)
print("Extracting XP data for screenshot players")
print("="*80)
print()

# Load servers
center_path = Path(r"R:\PhoenixArk\asaserver_center")
ragvegas_path = Path(r"R:\PhoenixArk\asaserver_ragvegas")

results = []

for map_name, server_path in [('center', center_path), ('RagVegas', ragvegas_path)]:
    if not server_path.exists():
        print(f"⚠️  {map_name} server not found at {server_path}")
        continue
    
    print(f"Loading {map_name} server...")
    try:
        reader = ArkSaveReader(server_path)
        players = reader.get_all_players()
        
        # Create lookup by name (case-insensitive)
        player_by_name = {}
        for p in players:
            if hasattr(p, 'character_name'):
                name = p.character_name.lower() if p.character_name else None
                if name:
                    player_by_name[name] = p
        
        # Match with screenshots
        for player_name, info in screenshot_players.items():
            if info['map'] != map_name:
                continue
            
            # Try to find player
            player = player_by_name.get(player_name.lower())
            
            if player:
                xp = player.experience if hasattr(player, 'experience') else 0
                level = info['level']
                
                results.append({
                    'name': player_name,
                    'level': level,
                    'xp': xp,
                    'map': map_name,
                    'eos_id': info['eos_id']
                })
                
                print(f"  ✓ {player_name:20s} L{level:3d} = {xp:>15,.0f} XP")
            else:
                print(f"  ✗ {player_name:20s} L{info['level']:3d} = NOT FOUND in save data")
        
        print()
    
    except Exception as e:
        print(f"  ❌ Error: {e}\n")

print("="*80)
print(f"Successfully extracted: {len(results)} players")
print("="*80)
print()

if results:
    # Sort by level
    results.sort(key=lambda x: x['level'])
    
    print("Summary (sorted by level):")
    print("-"*80)
    for r in results:
        print(f"L{r['level']:3d}: {r['xp']:>15,.0f} XP | {r['name']:20s} | {r['map']}")
    
    print()
    print("="*80)
    print("HIGH-LEVEL PLAYERS (L100+):")
    print("="*80)
    
    high_level = [r for r in results if r['level'] >= 100]
    if high_level:
        for r in high_level:
            print(f"  {r['name']:20s} L{r['level']:3d} = {r['xp']:>15,.0f} XP | {r['map']}")
        
        print()
        print(f"These {len(high_level)} high-level players will help refine the curve!")
    
    # Save to file for curve refinement
    with open('screenshot_players_center_ragvegas.txt', 'w') as f:
        f.write("# Players from Center and RagVegas screenshots\n")
        f.write("# Format: (level, xp, name, map)\n\n")
        f.write("screenshot_data = [\n")
        for r in results:
            f.write(f"    ({r['level']}, {r['xp']}, '{r['name']}', '{r['map']}'),\n")
        f.write("]\n")
    
    print(f"\n✓ Data saved to: screenshot_players_center_ragvegas.txt")

else:
    print("❌ No players found! Check that server paths are correct.")
