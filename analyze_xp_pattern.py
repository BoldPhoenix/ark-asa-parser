"""
Analyze the actual XP progression to understand the pattern.
"""

# Data points from Astraeos server
data_points = [
    (38, 7_129),
    (90, 612_400),
    (95, 975_649),
    (114, 6_179_425),
    (117, 7_541_021),
    (132, 28_614_060),
]

print("Analyzing XP progression patterns:")
print("="*70)

# Calculate XP per level and ratios
for i in range(len(data_points) - 1):
    level1, xp1 = data_points[i]
    level2, xp2 = data_points[i + 1]
    
    level_diff = level2 - level1
    xp_diff = xp2 - xp1
    xp_per_level = xp_diff / level_diff
    ratio = xp2 / xp1
    
    print(f"\nLevel {level1} → {level2} ({level_diff} levels):")
    print(f"  XP gained: {xp_diff:,}")
    print(f"  XP per level: {xp_per_level:,.0f}")
    print(f"  Total XP ratio: {ratio:.2f}x")
    print(f"  Implied multiplier per level: {ratio**(1/level_diff):.4f}")

print("\n" + "="*70)
print("\nTesting if there are different formulas for different level ranges:")
print("-"*70)

# Maybe low levels use vanilla table, high levels use modified?
# Let's see if levels 1-100 follow one pattern, 100+ follows another

print("\nLet me check if your server has custom XP multipliers...")
print("\nDo you have any XP multiplier settings in your server config?")
print("(OverridePlayerLevelEngramPoints, XPMultiplier, etc.)")
