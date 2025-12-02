"""
Reverse engineer ARK ASA XP multiplier using known data points.

Known data from BoldPhoenix:
- Current Level: 132
- Current XP: 28,615,150
- XP for Level 133: 33,373,538
"""

def calculate_base_xp_for_level(level):
    """Calculate base XP using formula: XP_Req = XP_Prev + 75 × 1.0015^Level"""
    xp = 0
    for lvl in range(2, level + 1):
        xp += 75 * (1.0015 ** lvl)
    return xp

# Calculate base XP requirements
base_xp_132 = calculate_base_xp_for_level(132)
base_xp_133 = calculate_base_xp_for_level(133)

print("=" * 80)
print("REVERSE ENGINEERING ARK ASA XP MULTIPLIER")
print("=" * 80)

print("\n1. Base Formula Calculation (no multiplier):")
print(f"   Level 132 base XP: {base_xp_132:,.2f}")
print(f"   Level 133 base XP: {base_xp_133:,.2f}")
print(f"   XP gain for level 132->133: {base_xp_133 - base_xp_132:,.2f}")

print("\n2. Actual Data from Game:")
print(f"   Current Level: 132")
print(f"   Current XP: 28,615,150")
print(f"   XP for Level 133: 33,373,538")
print(f"   XP needed to level up: {33373538 - 28615150:,}")

print("\n3. Calculate Multiplier:")
multiplier_current = 28615150 / base_xp_132
multiplier_next = 33373538 / base_xp_133

print(f"   Multiplier (current level): {multiplier_current:,.2f}x")
print(f"   Multiplier (next level): {multiplier_next:,.2f}x")
print(f"   Average multiplier: {(multiplier_current + multiplier_next) / 2:,.2f}x")

# Use average multiplier to build complete table
avg_multiplier = (multiplier_current + multiplier_next) / 2

print("\n4. Build Complete XP Table with Multiplier:")
xp_table = {}
for level in range(1, 201):
    base_xp = calculate_base_xp_for_level(level)
    actual_xp = base_xp * avg_multiplier
    xp_table[level] = actual_xp

print(f"\n   Sample levels with {avg_multiplier:,.2f}x multiplier:")
sample_levels = [1, 50, 100, 127, 132, 133, 150, 180, 200]
for lvl in sample_levels:
    if lvl in xp_table:
        print(f"   Level {lvl:3d}: {xp_table[lvl]:15,.0f} XP")

print("\n5. Verify Against Known Data:")
print(f"   Calculated XP for Level 132: {xp_table[132]:,.0f}")
print(f"   Actual XP (you have): 28,615,150")
print(f"   Difference: {abs(xp_table[132] - 28615150):,.0f} ({abs(xp_table[132] - 28615150) / 28615150 * 100:.2f}%)")

print(f"\n   Calculated XP for Level 133: {xp_table[133]:,.0f}")
print(f"   Actual XP needed: 33,373,538")
print(f"   Difference: {abs(xp_table[133] - 33373538):,.0f} ({abs(xp_table[133] - 33373538) / 33373538 * 100:.2f}%)")

print("\n6. Function to Convert XP to Level:")
def xp_to_level(xp, xp_table):
    """Convert XP to level using calculated table"""
    if xp <= 0:
        return 1
    
    for level in sorted(xp_table.keys(), reverse=True):
        if xp >= xp_table[level]:
            return level
    return 1

# Test with other known XP values
print("\n7. Test with Other Player XP Values:")
test_cases = [
    ("BoldPhoenix", 28615150, 132),
    ("Raven (lower)", 40635.04, None),
    ("Ataraxia", 357464.94, None),
    ("Mae", 10473538.00, None),
]

for name, xp, known_level in test_cases:
    calc_level = xp_to_level(xp, xp_table)
    if known_level:
        print(f"   {name}: XP={xp:,.0f} -> Level {calc_level} (expected: {known_level}) ✓" if calc_level == known_level else f"   {name}: XP={xp:,.0f} -> Level {calc_level} (expected: {known_level}) ✗")
    else:
        print(f"   {name}: XP={xp:,.0f} -> Level {calc_level}")

print("\n" + "=" * 80)
print(f"CONCLUSION: ARK ASA uses a {avg_multiplier:,.2f}x multiplier on base XP formula")
print("=" * 80)
