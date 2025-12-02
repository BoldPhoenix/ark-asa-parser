"""
Reverse engineer the exact ASA XP curve using real player data.

Given:
- Level 132 requires: 28,615,150 XP (current)
- Level 133 requires: 33,373,538 XP (next level)

The curve follows: XP[n] = XP[n-1] + (BaseXP * Multiplier^n)
"""

# Known data points from BoldPhoenix
current_level = 132
current_xp = 28615150
next_level_xp = 33373538

# Calculate the XP needed to go from 132 to 133
xp_for_next_level = next_level_xp - current_xp
print(f"XP needed to go from level {current_level} to {current_level + 1}: {xp_for_next_level:,}")

# Now we need to find BaseXP and Multiplier such that:
# XP_cost_for_level_133 = BaseXP * Multiplier^133

# Let's try to work backwards using the geometric progression formula
# If we assume the pattern from the script: cost = BaseXP * Multiplier^level

# Try different multipliers and see which gives us reasonable base XP values
print("\nTesting different multipliers:\n")

for mult in [1.10, 1.11, 1.115, 1.12, 1.13, 1.14, 1.15]:
    # If xp_for_next_level = BaseXP * mult^133
    # Then BaseXP = xp_for_next_level / mult^133
    base_xp = xp_for_next_level / (mult ** 133)
    
    # Now verify: what would level 132 cost?
    cost_for_132 = base_xp * (mult ** 132)
    
    # Calculate what level 132's TOTAL XP would be (sum of all costs up to 132)
    total_xp_at_132 = sum(base_xp * (mult ** i) for i in range(2, 133))
    
    error = abs(total_xp_at_132 - current_xp)
    error_pct = (error / current_xp) * 100
    
    print(f"Multiplier {mult:.3f}:")
    print(f"  Base XP: {base_xp:,.2f}")
    print(f"  Predicted total XP at 132: {total_xp_at_132:,.0f}")
    print(f"  Actual total XP at 132: {current_xp:,}")
    print(f"  Error: {error:,.0f} ({error_pct:.2f}%)")
    print()

# Now let's find the BEST multiplier by testing a finer range
print("\nFinding optimal multiplier:\n")

best_mult = 1.115
best_error = float('inf')

for mult_int in range(1110, 1160):  # Test 1.110 to 1.159
    mult = mult_int / 1000.0
    base_xp = xp_for_next_level / (mult ** 133)
    total_xp_at_132 = sum(base_xp * (mult ** i) for i in range(2, 133))
    error = abs(total_xp_at_132 - current_xp)
    
    if error < best_error:
        best_error = error
        best_mult = mult

print(f"Optimal multiplier: {best_mult:.4f}")
base_xp = xp_for_next_level / (best_mult ** 133)
print(f"Base XP: {base_xp:,.2f}")
print(f"Error: {best_error:,.0f} ({(best_error/current_xp)*100:.4f}%)")

# Calculate a few level checkpoints with this formula
print(f"\nPredicted XP requirements using multiplier {best_mult:.4f}:")
print("-" * 60)

cumulative = 0
for level in [1, 50, 100, 125, 130, 131, 132, 133, 134, 135, 140, 150]:
    if level == 1:
        print(f"Level {level:3d}: {cumulative:20,} XP")
    else:
        for i in range(2, level + 1):
            cumulative += base_xp * (best_mult ** i)
        print(f"Level {level:3d}: {cumulative:20,.0f} XP")
        cumulative = 0  # Reset for next checkpoint
