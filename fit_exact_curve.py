"""
Fit the exact XP curve using multiple real player data points from Astraeos.
"""

# Data points from Astraeos server (actual in-game levels from screenshots)
data_points = [
    # (level, xp, player_name)
    (38, 7_129, "Mëlkor"),  # From screenshot: Melbar level 38, but Melbar not in save - might be Mëlkor
    (90, 612_400, "Cassian"),
    (95, 975_649, "Sex4TRex"),
    (114, 6_179_425, "Joker"),
    (117, 7_541_021, "Panther"),
    (132, 28_614_060, "BoldPhoenix"),
]

print("Data points from Astraeos server:")
print("="*70)
for level, xp, name in data_points:
    print(f"Level {level:3d}: {xp:>12,} XP  ({name})")

print("\n" + "="*70)
print("\nFinding best multiplier using least squares...\n")

# Try to find multiplier that minimizes total error across ALL data points
# Use BoldPhoenix (level 132) as the reference since it's the highest level
best_mult = 0
best_error = float('inf')
best_base = 0

ref_level, ref_xp, ref_name = data_points[-1]  # Use last (highest level) as reference
print(f"Using {ref_name} (Level {ref_level}) as reference point\n")

for mult_int in range(1140, 1170):  # Test 1.140 to 1.169 (based on previous testing)
    mult = mult_int / 1000.0
    
    # Calculate base_xp from reference point
    total_mult_powers = sum(mult ** i for i in range(2, ref_level + 1))
    base_xp = ref_xp / total_mult_powers
    
    # Now test this base_xp against all data points
    total_error = 0
    for level, actual_xp, name in data_points:
        # Calculate predicted XP
        predicted_xp = sum(base_xp * (mult ** i) for i in range(2, level + 1))
        error = abs(predicted_xp - actual_xp)
        total_error += error
    
    if total_error < best_error:
        best_error = total_error
        best_mult = mult
        best_base = base_xp

print(f"Best multiplier: {best_mult:.3f}")
print(f"Best base XP: {best_base:.6f}")
print(f"Total error across all points: {best_error:,.0f}")

# Calculate average error percentage
avg_error_pct = 0
print("\nPredictions for each player:")
print("-" * 70)

for level, actual_xp, name in data_points:
    predicted_xp = sum(best_base * (best_mult ** i) for i in range(2, level + 1))
    error = abs(predicted_xp - actual_xp)
    error_pct = (error / actual_xp) * 100 if actual_xp > 0 else 0
    avg_error_pct += error_pct
    
    print(f"{name:20s} Level {level:3d}:")
    print(f"  Actual:    {actual_xp:>12,} XP")
    print(f"  Predicted: {predicted_xp:>12,.0f} XP")
    print(f"  Error:     {error:>12,.0f} ({error_pct:5.2f}%)")
    print()

avg_error_pct /= len(data_points)
print(f"Average error: {avg_error_pct:.2f}%")

# Build complete table with this multiplier
print("\n" + "="*70)
print("\nBuilding complete XP table...")

xp_table = {}
total_xp = 0
xp_table[1] = 0

for level in range(2, 201):
    xp_for_this_level = best_base * (best_mult ** level)
    total_xp += xp_for_this_level
    xp_table[level] = int(total_xp)

# Show key levels
print("\nKey levels:")
print(f"Level 100: {xp_table[100]:,}")
print(f"Level 132: {xp_table[132]:,} (BoldPhoenix actual: 28,614,060)")
print(f"Level 150: {xp_table[150]:,}")
print(f"Level 180: {xp_table[180]:,}")
print(f"Level 200: {xp_table[200]:,}")

# Save to file
with open("ark_asa_xp_table_final.txt", "w", encoding="utf-8") as f:
    f.write(f"# ARK ASA XP Table (Multi-point fitted)\n")
    f.write(f"# Multiplier: {best_mult:.3f}\n")
    f.write(f"# Base XP: {best_base:.6f}\n")
    f.write(f"# Average error: {avg_error_pct:.2f}%\n\n")
    f.write("ARK_ASA_XP_TABLE = {\n")
    for level in range(1, 201):
        if level % 10 == 1:
            f.write("    ")
        f.write(f"{level}: {xp_table[level]}, ")
        if level % 10 == 0:
            f.write("\n")
    f.write("}\n")

print("\nTable saved to: ark_asa_xp_table_final.txt")
