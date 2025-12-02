"""
Fit exact XP curve using comprehensive dataset (20 players, levels 1-132).
"""

# Complete dataset from both servers
data_points = [
    (1, 11, 'Beyonx'),
    (1, 42, 'oTomadorDeTerere'),
    (9, 877, 'Rhyno'),
    (15, 1141, 'Tester'),
    (25, 3117, 'LionsLord'),
    (38, 7129, 'Mëlkor'),
    (64, 28091, 'Aatxe'),
    (71, 55484, 'Dc kid'),
    (78, 146580, 'Raven Yuri'),
    (82, 259671, 'Reina'),
    (88, 497641, 'Poli'),
    (90, 612400, 'Cassian'),
    (95, 975649, 'Sex4TRex'),
    (97, 1259269, 'Jake'),
    (105, 4098538, 'Bundy'),
    (105, 4098538, 'May'),
    (114, 6179425, 'Joker'),
    (117, 7541021, 'Panther'),
    (131, 20947286, 'Jaxxx'),
    (132, 28614060, 'BoldPhoenix'),
]

print(f"Fitting XP curve with {len(data_points)} data points")
print("="*70)

# Use a high-level player as reference (level 132)
ref_level, ref_xp, ref_name = data_points[-1]
print(f"Reference: {ref_name} (Level {ref_level}, {ref_xp:,} XP)\n")

best_mult = 0
best_error = float('inf')
best_base = 0
best_avg_error_pct = 100

# Test range around 1.15 based on previous findings
for mult_int in range(1100, 1200):  # 1.100 to 1.199
    mult = mult_int / 1000.0
    
    # Calculate base_xp from reference point
    total_mult_powers = sum(mult ** i for i in range(2, ref_level + 1))
    base_xp = ref_xp / total_mult_powers
    
    # Calculate error across all data points
    total_error = 0
    total_error_pct = 0
    valid_points = 0
    
    for level, actual_xp, name in data_points:
        if actual_xp < 100:  # Skip very low XP values (level 1 players)
            continue
        
        predicted_xp = sum(base_xp * (mult ** i) for i in range(2, level + 1))
        error = abs(predicted_xp - actual_xp)
        error_pct = (error / actual_xp) * 100
        
        total_error += error
        total_error_pct += error_pct
        valid_points += 1
    
    avg_error_pct = total_error_pct / valid_points if valid_points > 0 else 100
    
    if avg_error_pct < best_avg_error_pct:
        best_avg_error_pct = avg_error_pct
        best_error = total_error
        best_mult = mult
        best_base = base_xp

print(f"Best multiplier: {best_mult:.4f}")
print(f"Best base XP: {best_base:.8f}")
print(f"Average error: {best_avg_error_pct:.2f}%")
print(f"Total absolute error: {best_error:,.0f}")

print("\n" + "="*70)
print("\nValidation against all data points:")
print("-"*70)

# Test predictions
max_error_pct = 0
max_error_player = ""

for level, actual_xp, name in data_points:
    if actual_xp < 100:  # Skip level 1
        continue
    
    predicted_xp = sum(best_base * (best_mult ** i) for i in range(2, level + 1))
    error = abs(predicted_xp - actual_xp)
    error_pct = (error / actual_xp) * 100
    
    if error_pct > max_error_pct:
        max_error_pct = error_pct
        max_error_player = name
    
    status = "✓" if error_pct < 10 else "✗"
    print(f"{status} {name:20s} L{level:3d} | Actual: {actual_xp:>12,} | Pred: {predicted_xp:>12,.0f} | Err: {error_pct:5.1f}%")

print("\n" + "="*70)
print(f"\nWorst prediction: {max_error_player} ({max_error_pct:.2f}% error)")

# Build complete XP table
print("\nBuilding complete XP table...")

xp_table = {1: 0}
total_xp = 0

for level in range(2, 201):
    xp_for_this_level = best_base * (best_mult ** level)
    total_xp += xp_for_this_level
    xp_table[level] = int(total_xp)

print(f"\nKey levels:")
print(f"Level  50: {xp_table[50]:,}")
print(f"Level 100: {xp_table[100]:,}")
print(f"Level 132: {xp_table[132]:,} (actual: 28,614,060)")
print(f"Level 150: {xp_table[150]:,}")
print(f"Level 180: {xp_table[180]:,}")

# Save Python-formatted table
with open("final_xp_table.txt", "w", encoding="utf-8") as f:
    f.write(f"# ARK ASA XP Table (Fitted from 20 players, levels 1-132)\n")
    f.write(f"# Multiplier: {best_mult:.4f}\n")
    f.write(f"# Base XP: {best_base:.8f}\n")
    f.write(f"# Average error: {best_avg_error_pct:.2f}%\n\n")
    f.write("ARK_ASA_XP_TABLE = {\n")
    for level in range(1, 201):
        if level % 10 == 1:
            f.write("    ")
        f.write(f"{level}: {xp_table[level]}, ")
        if level % 10 == 0:
            f.write("\n")
    f.write("}\n")

print(f"\nTable saved to: final_xp_table.txt")
