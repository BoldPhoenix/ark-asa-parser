"""
Try to match the EXACT XP curve by testing if there's a different base formula.

ARK might be using a modified version of the geometric progression.
Let's try: XP_total[n] = sum(BaseXP * Multiplier^(i + offset))
"""

current_level = 132
current_xp = 28615150
next_level_xp = 33373538
xp_for_level_133 = next_level_xp - current_xp

print("Testing with level offset adjustments:\n")

# Try different offsets (ARK might not start at level 2)
for offset in range(-10, 20):
    for mult_int in range(1140, 1180):
        mult = mult_int / 1000.0
        
        # Calculate base XP based on what level 133 costs
        # xp_for_level_133 = BaseXP * mult^(133 + offset)
        base_xp = xp_for_level_133 / (mult ** (133 + offset))
        
        # Calculate total XP up to level 132
        total_xp = 0
        for level in range(2, 133):  # Start from level 2 (level 1 = 0 XP)
            total_xp += base_xp * (mult ** (level + offset))
        
        error = abs(total_xp - current_xp)
        error_pct = (error / current_xp) * 100
        
        if error_pct < 0.1:  # Less than 0.1% error
            print(f"EXCELLENT MATCH!")
            print(f"  Multiplier: {mult:.3f}")
            print(f"  Offset: {offset}")
            print(f"  Base XP: {base_xp:.4f}")
            print(f"  Predicted XP at 132: {total_xp:,.0f}")
            print(f"  Actual XP at 132: {current_xp:,}")
            print(f"  Error: {error:,.0f} ({error_pct:.4f}%)")
            print()
            
            # Test prediction for next level
            xp_for_133_calc = base_xp * (mult ** (133 + offset))
            predicted_next = total_xp + xp_for_133_calc
            print(f"  Predicted XP at 133: {predicted_next:,.0f}")
            print(f"  Actual XP at 133: {next_level_xp:,}")
            print(f"  Next level error: {abs(predicted_next - next_level_xp):,.0f}")
            print("\n" + "=" * 70 + "\n")

print("\nSearching for best match...")
