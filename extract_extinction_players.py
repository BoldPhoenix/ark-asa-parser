"""
Extract XP data for Extinction players from screenshots
Check both live PhoenixArk and arkbackups folders
"""

from pathlib import Path
from ark_asa_parser import ArkSaveReader

# Players from Extinction screenshots
extinction_players = {
    'Buzz': {'eos_id': '7141017', 'level': 105},
    'Human': {'eos_id': '195147359', 'level': 88},
    'Donatello': {'eos_id': '747951672', 'level': 1},
    'NikitaLina': {'eos_id': '895580949', 'level': 105},
    'Connor McGregor': {'eos_id': '77191826', 'level': 105},
    'Sunniva': {'eos_id': '49651294', 'level': 134},
}

print("="*80)
print("Extracting XP data for Extinction players")
print("="*80)
print()

# Check both locations
locations = [
    (Path(r"R:\PhoenixArk\asaserver_extinction"), "Live PhoenixArk"),
    (Path(r"X:\Extinction\Extinction_WP"), "X_Backup"),
]

results = []

for server_path, location_name in locations:
    if not server_path.exists():
        print(f"⚠️  {location_name} Extinction not found at {server_path}")
        continue
    
    print(f"Checking {location_name} Extinction server...")
    print("-"*80)
    
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
        found_in_location = []
        for player_name, info in extinction_players.items():
            # Skip if already found in previous location
            if any(r['name'] == player_name for r in results):
                continue
            
            player = player_by_name.get(player_name.lower())
            
            if player:
                xp = player.experience if hasattr(player, 'experience') else 0
                level = info['level']
                
                result = {
                    'name': player_name,
                    'level': level,
                    'xp': xp,
                    'map': 'extinction',
                    'location': location_name,
                    'eos_id': info['eos_id']
                }
                results.append(result)
                found_in_location.append(result)
                
                print(f"  ✓ {player_name:20s} L{level:3d} = {xp:>15,.0f} XP")
            else:
                print(f"  ✗ {player_name:20s} L{info['level']:3d} = NOT FOUND")
        
        if found_in_location:
            print(f"\n  Found {len(found_in_location)} players in {location_name}")
        print()
    
    except Exception as e:
        print(f"  ❌ Error: {e}\n")

print("="*80)
print(f"Total extracted: {len(results)} players")
print("="*80)
print()

if results:
    # Sort by level
    results.sort(key=lambda x: x['level'])
    
    print("Summary (sorted by level):")
    print("-"*80)
    for r in results:
        print(f"L{r['level']:3d}: {r['xp']:>15,.0f} XP | {r['name']:20s} | {r['location']}")
    
    print()
    print("="*80)
    print("HIGH-LEVEL PLAYERS (L100+):")
    print("="*80)
    
    high_level = [r for r in results if r['level'] >= 100]
    if high_level:
        for r in high_level:
            print(f"  {r['name']:20s} L{r['level']:3d} = {r['xp']:>15,.0f} XP | {r['location']}")
        
        print()
        print(f"✓ These {len(high_level)} high-level players add to our dataset!")
    
    # Check for Sunniva specifically (L134 - same as LadySif!)
    sunniva = next((r for r in results if r['name'] == 'Sunniva'), None)
    if sunniva:
        print()
        print("="*80)
        print("CRITICAL DATA POINT:")
        print("="*80)
        print(f"Sunniva L134 = {sunniva['xp']:,.0f} XP")
        print(f"LadySif L134 = 51,915,584 XP (from Amissa)")
        print()
        if abs(sunniva['xp'] - 51915584) / 51915584 < 0.1:
            print("✓ XP values are very close! Validates our L134 data point.")
        else:
            diff = sunniva['xp'] - 51915584
            pct = (diff / 51915584) * 100
            print(f"⚠️  XP differs by {diff:,.0f} ({pct:+.1f}%)")
            if diff < 0:
                print("   Sunniva might have used level boosts (explorer notes/bosses)")
            else:
                print("   Sunniva might have pure-ground more than LadySif")
    
    # Save to file
    with open('extinction_screenshot_players.txt', 'w') as f:
        f.write("# Players from Extinction screenshots\n")
        f.write("# Format: (level, xp, name, location)\n\n")
        f.write("extinction_data = [\n")
        for r in results:
            f.write(f"    ({r['level']}, {r['xp']}, '{r['name']}', '{r['location']}'),\n")
        f.write("]\n")
    
    print(f"\n✓ Data saved to: extinction_screenshot_players.txt")

else:
    print("❌ No players found! Checking other backup locations...")
    print()
    print("Other possible locations to check:")
    print("  - R:\\ArkBackups\\")
    print("  - D:\\ArkBackups\\ark\\")
    print("  - X:\\PhoenixArk\\")
