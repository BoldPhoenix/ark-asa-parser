"""
Try to find if the multiplier follows a pattern based on level.

We know:
- Level 132: 28,615,150 XP (actual)
- Level 133: 33,373,538 XP (actual)
- Base formula: XP_Req = XP_Prev + 75 × 1.0015^Level

Maybe the scalar increases with level too?
"""

def calculate_base_xp_cumulative(level):
    """Calculate cumulative base XP for a level"""
    xp = 0
    for lvl in range(2, level + 1):
        xp += 75 * (1.0015 ** lvl)
    return xp

# We have two data points - let's see the pattern
base_132 = calculate_base_xp_cumulative(132)
base_133 = calculate_base_xp_cumulative(133)

actual_132 = 28615150
actual_133 = 33373538

mult_132 = actual_132 / base_132
mult_133 = actual_133 / base_133

print("Multiplier by Level:")
print(f"Level 132: {mult_132:.2f}x")
print(f"Level 133: {mult_133:.2f}x")
print(f"Increase: {mult_133 - mult_132:.2f}x per level")
print(f"Increase rate: {(mult_133 - mult_132) / mult_132 * 100:.4f}% per level")

# Maybe the multiplier follows: multiplier = base_mult * (1 + growth_rate)^level
# Let's calculate what that growth rate would be
growth_rate = (mult_133 / mult_132) - 1
print(f"\nIf multiplier grows exponentially:")
print(f"Growth rate per level: {growth_rate * 100:.4f}%")

# Try to extrapolate to other levels
print(f"\nExtrapolating multipliers:")
# Start from level 132
mult_at_level = {}
for level in range(1, 201):
    if level == 132:
        mult_at_level[level] = mult_132
    elif level < 132:
        # Work backwards
        levels_diff = 132 - level
        mult_at_level[level] = mult_132 / ((1 + growth_rate) ** levels_diff)
    else:
        # Work forwards
        levels_diff = level - 132
        mult_at_level[level] = mult_132 * ((1 + growth_rate) ** levels_diff)

# Build full XP table
xp_table = {}
for level in range(1, 201):
    base_xp = calculate_base_xp_cumulative(level)
    multiplier = mult_at_level[level]
    xp_table[level] = base_xp * multiplier

print(f"\nSample XP requirements with variable multiplier:")
sample_levels = [50, 100, 127, 132, 133, 150, 180, 200]
for lvl in sample_levels:
    print(f"Level {lvl:3d}: {xp_table[lvl]:15,.0f} XP (multiplier: {mult_at_level[lvl]:.2f}x)")

print(f"\n\nVerification against known values:")
print(f"Level 132 calculated: {xp_table[132]:,.0f}")
print(f"Level 132 actual:     28,615,150")
print(f"Match: {'✓' if abs(xp_table[132] - 28615150) < 1000 else '✗'}")

print(f"\nLevel 133 calculated: {xp_table[133]:,.0f}")
print(f"Level 133 actual:     33,373,538")
print(f"Match: {'✓' if abs(xp_table[133] - 33373538) < 1000 else '✗'}")

# Now test with other player XP values
def xp_to_level(xp, xp_table):
    if xp <= 0:
        return 1
    for level in sorted(xp_table.keys(), reverse=True):
        if xp >= xp_table[level]:
            return level
    return 1

print(f"\n\nTesting with other players:")
test_players = [
    ("Raven", 40635.04),
    ("Ataraxia", 357464.94),
    ("Mae", 10473538.00),
]

for name, xp in test_players:
    level = xp_to_level(xp, xp_table)
    print(f"{name:15s}: XP={xp:12,.0f} -> Level {level:3d} (multiplier at that level: {mult_at_level[level]:.2f}x)")
