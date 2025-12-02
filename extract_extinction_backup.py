"""
Extract Extinction players from X:\ backup drive
Looking for: Sunniva (L134), Connor McGregor, Buzz, NikitaLina, Human (L105, L88)
"""

from pathlib import Path
from ark_asa_parser import ArkSaveReader

# Players from screenshots
extinction_players = {
    'Buzz': 105,
    'Human': 88,
    'Donatello': 1,
    'NikitaLina': 105,
    'Connor McGregor': 105,
    'Sunniva': 134,  # CRITICAL - same level as LadySif!
}

print("="*80)
print("Extracting Extinction players from X:\\ backup")
print("="*80)
print()

# Check X:\Extinction
extinction_path = Path(r"X:\Extinction")

if not extinction_path.exists():
    print(f"❌ Extinction backup not found at {extinction_path}")
    exit(1)

print(f"Loading from: {extinction_path}")
print("-"*80)

try:
    reader = ArkSaveReader(extinction_path)
    players = reader.get_all_players()
    
    # Create lookup
    player_by_name = {}
    for p in players:
        if hasattr(p, 'character_name') and p.character_name:
            player_by_name[p.character_name.lower()] = p
    
    print(f"Total players in backup: {len(players)}")
    print()
    
    # Match screenshot players
    results = []
    for player_name, expected_level in sorted(extinction_players.items(), key=lambda x: x[1], reverse=True):
        player = player_by_name.get(player_name.lower())
        
        if player:
            xp = player.experience if hasattr(player, 'experience') else 0
            results.append((player_name, expected_level, xp))
            print(f"✓ {player_name:20s} L{expected_level:3d} = {xp:>15,.0f} XP")
        else:
            print(f"✗ {player_name:20s} L{expected_level:3d} = NOT FOUND")
    
    print()
    print("="*80)
    print("ANALYSIS:")
    print("="*80)
    print()
    
    if results:
        # Focus on high-level players
        high_level = [(n, l, x) for n, l, x in results if l >= 100]
        
        if high_level:
            print("High-level players (L100+):")
            print("-"*80)
            for name, level, xp in high_level:
                print(f"  {name:20s} L{level:3d} = {xp:>15,.0f} XP")
            
            # Compare Sunniva with LadySif
            sunniva = next((r for r in results if r[0] == 'Sunniva'), None)
            if sunniva:
                print()
                print("="*80)
                print("CRITICAL COMPARISON - Two L134 players:")
                print("="*80)
                ladysif_xp = 51915584.0
                sunniva_xp = sunniva[2]
                
                print(f"  LadySif (Amissa):      {ladysif_xp:>15,.0f} XP")
                print(f"  Sunniva (Extinction):  {sunniva_xp:>15,.0f} XP")
                
                if sunniva_xp > 0:
                    diff = sunniva_xp - ladysif_xp
                    pct = (diff / ladysif_xp) * 100
                    
                    print()
                    print(f"  Difference:            {diff:>15,.0f} XP ({pct:+.1f}%)")
                    print()
                    
                    if abs(pct) < 5:
                        print("  ✓ Very close! Both around same XP for L134")
                        print("  ✓ Validates our L134 data point")
                    elif sunniva_xp < ladysif_xp:
                        print("  ⚠️  Sunniva has LESS XP → likely used level boosts")
                        print("  → Should use LadySif as pure grind baseline")
                    else:
                        print("  ✓ Sunniva has MORE XP → more pure grinding")
                        print("  → Should use Sunniva as pure grind baseline")
        
        # Save results
        print()
        with open('extinction_backup_data.txt', 'w') as f:
            f.write("# Extinction players from X:\\ backup\n")
            f.write("# Format: (level, xp, name)\n\n")
            f.write("extinction_backup_data = [\n")
            for name, level, xp in sorted(results, key=lambda x: x[1]):
                f.write(f"    ({level}, {xp}, '{name}'),\n")
            f.write("]\n")
        
        print(f"✓ Data saved to: extinction_backup_data.txt")
    
    else:
        print("❌ No screenshot players found in backup")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print()
print("="*80)
print("NEXT STEP: Pure Grind Character")
print("="*80)
print("""
Creating a NEW character with PURE grinding (no boosts) is EXCELLENT!

Recommendation for data collection:
1. Create character, note starting level (1)
2. Every 5-10 levels, take screenshot showing:
   - Current level
   - Current XP (from character screen)
3. Record data in format: Level X = Y XP
4. Go as high as possible (ideally to L100+)

This will give us EXACT baseline values to validate/refine the curve!

Suggested format for recording:
  Level 1 = 0 XP
  Level 5 = 234 XP
  Level 10 = 1,234 XP
  Level 20 = 12,345 XP
  etc.

Save to a text file and I'll use it to recalculate the optimal curve.
""")
