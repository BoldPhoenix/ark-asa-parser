"""Generate final XP table for analytics dashboard"""

def calculate_xp_for_level(level, multiplier=1.1050, base_xp=6.59849716):
    if level <= 1:
        return 0
    return int(sum(base_xp * (multiplier ** i) for i in range(2, level + 1)))

print("# ARK ASA XP Table - Reverse-engineered from 24 pure grind players")
print("# Multiplier: 1.1050, Base XP: 6.59849716")
print("# Accuracy: Perfect at L114, ±1-2 for high levels (L134-143)")
print("# Based on max XP per level (pure grind path, no level boosts)")
print()
print("ARK_ASA_XP_TABLE = {")
for level in range(1, 201):
    xp = calculate_xp_for_level(level)
    print(f"    {level}: {xp},")
print("}")
