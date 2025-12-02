"""
Final curve fitting - weight higher level players more heavily.
Focus on players level 110+ where data is more reliable.
"""

# Complete dataset
all_data = [
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
    (105, 4098538, 'Bundy'),  # Suspicious - exact same XP
    (105, 4098538, 'May'),     # Suspicious - exact same XP
    (114, 6179425, 'Joker'),
    (117, 7541021, 'Panther'),
    (131, 20947286, 'Jaxxx'),
    (132, 28614060, 'BoldPhoenix'),
]

# Focus on high-level players (110+) as reference
high_level_players = [(l, xp, n) for l, xp, n in all_data if l >= 110]

print("High-level players (most reliable data):")
for level, xp, name in high_level_players:
    print(f"  Level {level}: {xp:,} XP ({name})")

print("\n" + "="*70)
print("\nFitting curve using level 132 as reference...")
print("Testing multipliers to minimize error on high-level players\n")

ref_level, ref_xp, ref_name = high_level_players[-1]  # BoldPhoenix

best_mult = 0
best_error_high = float('inf')
best_base = 0

for mult_int in range(1100, 1200):
    mult = mult_int / 1000.0
    
    # Calculate base_xp from BoldPhoenix
    total_mult_powers = sum(mult ** i for i in range(2, ref_level + 1))
    base_xp = ref_xp / total_mult_powers
    
    # Calculate error on HIGH LEVEL players only
    error_high = 0
    for level, actual_xp, name in high_level_players:
        predicted_xp = sum(base_xp * (mult ** i) for i in range(2, level + 1))
        error_high += abs(predicted_xp - actual_xp)
    
    if error_high < best_error_high:
        best_error_high = error_high
        best_mult = mult
        best_base = base_xp

print(f"Best multiplier: {best_mult:.4f}")
print(f"Best base XP: {best_base:.8f}")
print(f"Error on high-level players: {best_error_high:,.0f}")

print("\n" + "="*70)
print("\nPredictions for ALL players:")
print("-"*70)

total_error_pct = 0
valid_count = 0

for level, actual_xp, name in all_data:
    predicted_xp = sum(best_base * (best_mult ** i) for i in range(2, level + 1))
    error = abs(predicted_xp - actual_xp)
    error_pct = (error / actual_xp) * 100 if actual_xp > 0 else 0
    
    if level >= 70:  # Only count mid-high level for average
        total_error_pct += error_pct
        valid_count += 1
    
    status = "✓" if error_pct < 15 else ("~" if error_pct < 30 else "✗")
    print(f"{status} L{level:3d} {name:20s} | Actual: {actual_xp:>12,} | Pred: {predicted_xp:>12,.0f} | Err: {error_pct:5.1f}%")

avg_error = total_error_pct / valid_count if valid_count > 0 else 0
print(f"\nAverage error (levels 70+): {avg_error:.2f}%")

# Build XP table
xp_table = {1: 0}
total_xp = 0

for level in range(2, 201):
    xp_for_this_level = best_base * (best_mult ** level)
    total_xp += xp_for_this_level
    xp_table[level] = int(total_xp)

print("\n" + "="*70)
print("\nFinal XP Table (key levels):")
print(f"Level  50: {xp_table[50]:,}")
print(f"Level 100: {xp_table[100]:,}")
print(f"Level 132: {xp_table[132]:,} (BoldPhoenix actual: 28,614,060)")
print(f"Level 150: {xp_table[150]:,}")
print(f"Level 180: {xp_table[180]:,}")
print(f"Level 200: {xp_table[200]:,}")

# Test reverse lookup
print("\n" + "="*70)
print("\nTesting reverse XP→Level lookup:")
test_xp_values = [28614060, 7541021, 1259269, 146580]
for test_xp in test_xp_values:
    for level in range(1, 200):
        if xp_table.get(level + 1, float('inf')) > test_xp >= xp_table[level]:
            print(f"  {test_xp:>12,} XP → Level {level}")
            break

print("\n✓ Curve fitting complete!")
print(f"  Multiplier: {best_mult:.4f}")
print(f"  Base XP: {best_base:.8f}")
print(f"  Accuracy: ~{100-avg_error:.1f}% for levels 70+")
