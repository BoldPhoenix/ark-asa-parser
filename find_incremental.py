"""
Test if ARK uses: XP_for_level[n] = XP_for_level[n-1] * multiplier + base_increment

This would be similar to the community formula but with a multiplier on the previous cost.
"""

current_level = 132
current_xp = 28615150
next_level_xp = 33373538
xp_for_level_133 = next_level_xp - current_xp

print(f"XP cost for level 132→133: {xp_for_level_133:,}\n")

# Try: cost_n = cost_(n-1) * mult + base
# Given we know level 133 costs 4,758,388
# We need to work backwards to find what level 132 cost, then 131, etc.

print("Testing multiplicative increment formula:\n")

best_error = float('inf')
best_mult = 0
best_base = 0
best_start = 0

# Test different starting XP for level 2
for start_xp in [75, 100, 125, 150, 200, 250, 300, 350, 400, 450, 500]:
    # Test different multipliers
    for mult_int in range(10015, 10100):  # 1.0015 to 1.0099
        mult = mult_int / 10000.0
        
        # Test different base increments
        for base in [0, 25, 50, 75, 100]:
            # Build XP curve from level 2 to 132
            xp_costs = [0, 0, start_xp]  # Level 0, 1, 2
            
            for level in range(3, 134):
                cost = xp_costs[level - 1] * mult + base
                xp_costs.append(cost)
            
            # Calculate total XP at level 132
            total_xp = sum(xp_costs[2:133])  # Sum from level 2 to 132
            
            error = abs(total_xp - current_xp)
            error_pct = (error / current_xp) * 100
            
            if error < best_error:
                best_error = error
                best_mult = mult
                best_base = base
                best_start = start_xp
            
            if error_pct < 1.0:  # Less than 1% error
                print(f"Good match:")
                print(f"  Multiplier: {mult:.4f}")
                print(f"  Base increment: {base}")
                print(f"  Starting XP (level 2): {start_xp}")
                print(f"  Predicted XP at 132: {total_xp:,.0f}")
                print(f"  Actual XP at 132: {current_xp:,}")
                print(f"  Error: {error:,.0f} ({error_pct:.4f}%)")
                print(f"  Cost of level 133: {xp_costs[133]:,.0f} (actual: {xp_for_level_133:,})")
                print()

print(f"\nBest match found:")
print(f"  Multiplier: {best_mult:.4f}")
print(f"  Base increment: {best_base}")
print(f"  Starting XP (level 2): {best_start}")
print(f"  Error: {best_error:,.0f} ({(best_error/current_xp)*100:.4f}%)")
