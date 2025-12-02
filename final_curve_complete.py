"""
Final curve fitting with complete dataset including high-level players 143 and 134.
"""

# Complete dataset with Amissa high-level players
all_data = [
    # Previous data
    (9, 877, 'Rhyno'),
    (15, 1141, 'Tester'),
    (20, 2097, 'Ami Fallen'),
    (21, 2287, 'Tapeworm'),
    (25, 3117, 'LionsLord'),
    (38, 7129, 'Mëlkor'),
    (39, 9178, 'Eos'),
    (64, 28091, 'Aatxe'),
    (68, 39440, 'Sevey'),
    (71, 55484, 'Dc kid'),
    (71, 95386, 'Robf73'),
    (74, 95386, 'Robf73'),  # Using screenshot level
    (78, 146580, 'Raven Yuri'),
    (82, 259671, 'Reina'),
    (83, 280700, 'ShadiDK'),
    (88, 497641, 'Poli'),
    (89, 549541, 'Anjo'),
    (89, 564969, 'Lex XD'),
    (90, 612400, 'Cassian'),
    (90, 424092, 'Cassian Amissa'),  # Same player, different server
    (95, 975649, 'Sex4TRex'),
    (96, 1107272, 'Mathias'),
    (97, 1259269, 'Jake'),
    (114, 6179425, 'Joker'),
    (117, 7541021, 'Panther'),
    (131, 20947286, 'Jaxxx'),
    (132, 28614060, 'BoldPhoenix'),
    (134, 51915584, 'LadySif'),  # HIGH LEVEL!
    (143, 142988992, 'Axl'),  # HIGHEST LEVEL!
]

print("Complete dataset with HIGH-LEVEL players:")
print("="*70)
print(f"Total data points: {len(all_data)}")
print(f"Level range: {min(d[0] for d in all_data)} - {max(d[0] for d in all_data)}")
print()

# Show high-level players
print("Critical high-level data points:")
print("-"*70)
for level, xp, name in sorted(all_data, key=lambda x: x[0], reverse=True)[:5]:
    print(f"★ Level {level:3d}: {xp:>13,} XP  ({name})")

print("\n" + "="*70)
print("\nFitting curve using level 143 (Axl) as reference point...")

ref_level = 143
ref_xp = 142988992

best_mult = 0
best_base = 0
best_total_error = float('inf')

# Test multipliers
for mult_int in range(1090, 1120):  # 1.090 to 1.119
    mult = mult_int / 1000.0
    
    # Calculate base_xp from Axl (level 143)
    total_mult_powers = sum(mult ** i for i in range(2, ref_level + 1))
    base_xp = ref_xp / total_mult_powers
    
    # Calculate total error across ALL data points (weighted by level)
    total_error = 0
    for level, actual_xp, name in all_data:
        if level < 20:  # Skip very low levels
            continue
        
        predicted_xp = sum(base_xp * (mult ** i) for i in range(2, level + 1))
        error = abs(predicted_xp - actual_xp)
        
        # Weight higher level players more heavily
        weight = 1.0 if level < 100 else (2.0 if level < 130 else 3.0)
        total_error += error * weight
    
    if total_error < best_total_error:
        best_total_error = total_error
        best_mult = mult
        best_base = base_xp

print(f"\nBest multiplier: {best_mult:.4f}")
print(f"Best base XP: {best_base:.8f}")
print(f"Weighted total error: {best_total_error:,.0f}")

print("\n" + "="*70)
print("\nValidation against all data points:")
print("-"*70)

total_error_pct = 0
valid_count = 0

for level, actual_xp, name in sorted(all_data, key=lambda x: x[0]):
    if level < 20:
        continue
    
    predicted_xp = sum(best_base * (best_mult ** i) for i in range(2, level + 1))
    error = abs(predicted_xp - actual_xp)
    error_pct = (error / actual_xp) * 100 if actual_xp > 0 else 0
    
    if level >= 70:
        total_error_pct += error_pct
        valid_count += 1
    
    status = "✓" if error_pct < 10 else ("~" if error_pct < 20 else "✗")
    highlight = "★" if level >= 130 else " "
    
    print(f"{highlight}{status} L{level:3d} {name:20s} | Actual: {actual_xp:>13,} | Pred: {predicted_xp:>13,.0f} | Err: {error_pct:5.1f}%")

avg_error = total_error_pct / valid_count if valid_count > 0 else 0
print(f"\nAverage error (levels 70+): {avg_error:.2f}%")
print(f"Accuracy: {100-avg_error:.1f}%")

# Build final XP table
print("\n" + "="*70)
print("\nBuilding final XP table...")

xp_table = {1: 0}
total_xp = 0

for level in range(2, 201):
    xp_for_this_level = best_base * (best_mult ** level)
    total_xp += xp_for_this_level
    xp_table[level] = int(total_xp)

print(f"\nKey levels:")
print(f"Level  50: {xp_table[50]:,}")
print(f"Level 100: {xp_table[100]:,}")
print(f"Level 132: {xp_table[132]:,} (BoldPhoenix: 28,614,060)")
print(f"Level 134: {xp_table[134]:,} (LadySif: 51,915,584)")
print(f"Level 143: {xp_table[143]:,} (Axl: 142,988,992)")
print(f"Level 150: {xp_table[150]:,}")
print(f"Level 180: {xp_table[180]:,}")
print(f"Level 200: {xp_table[200]:,}")

# Test reverse lookup
print("\n" + "="*70)
print("\nReverse XP→Level predictions:")
test_cases = [
    (142988992, 143, "Axl"),
    (51915584, 134, "LadySif"),
    (28614060, 132, "BoldPhoenix"),
    (7541021, 117, "Panther"),
]

for test_xp, actual_level, name in test_cases:
    for level in range(1, 200):
        if xp_table.get(level + 1, float('inf')) > test_xp >= xp_table[level]:
            diff = level - actual_level
            status = "✓" if diff == 0 else f"({diff:+d})"
            print(f"  {name:15s} {test_xp:>13,} XP → Level {level:3d} {status} (actual: {actual_level})")
            break

print("\n✓ Final curve complete!")
print(f"  Multiplier: {best_mult:.4f}")
print(f"  Base XP: {best_base:.8f}")
print(f"  Accuracy: ~{100-avg_error:.1f}% for levels 70-143")
