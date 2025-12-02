"""Read Amissa players from X: drive backup."""
from pathlib import Path
from ark_asa_parser import ArkSaveReader

reader = ArkSaveReader(Path(r'X:\Amissa\Amissa'))
players = reader.get_all_players()

print(f'Found {len(players)} players on Amissa\n')
print('='*70)

# Sort by level descending
sorted_players = sorted(players, key=lambda x: x.level if hasattr(x, 'level') and x.level else 0, reverse=True)

for p in sorted_players[:30]:
    if hasattr(p, 'character_name') and p.character_name:
        name = p.character_name
        level = p.level if hasattr(p, 'level') else 0
        xp = p.experience if hasattr(p, 'experience') else 0
        print(f'{name:20s} Level {level:3d} | {xp:>12,.0f} XP')
