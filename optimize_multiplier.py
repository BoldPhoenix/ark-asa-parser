"""
Try finding the best overall multiplier by minimizing error across critical levels.
"""

critical_data = [
    (117, 7541021, 'Panther'),
    (132, 28614060, 'BoldPhoenix'),
    (134, 51915584, 'LadySif'),
    (143, 142988992, 'Axl'),
]

print("Finding optimal multiplier for high-level accuracy...")
print("="*70)

best_mult = 0
best_base = 0
best_avg_error = float('inf')

for mult_int in range(1100, 1150):
    mult = mult_int / 1000.0
    
    # Calculate base_xp for each reference, then average
    bases = []
    for ref_level, ref_xp, name in critical_data:
        total_mult_powers = sum(mult ** i for i in range(2, ref_level + 1))
        base_xp = ref_xp / total_mult_powers
        bases.append(base_xp)
    
    avg_base = sum(bases) / len(bases)
    
    # Test this against all critical points
    total_error_pct = 0
    for level, actual_xp, name in critical_data:
        predicted_xp = sum(avg_base * (mult ** i) for i in range(2, level + 1))
        error_pct = abs(predicted_xp - actual_xp) / actual_xp * 100
        total_error_pct += error_pct
    
    avg_error_pct = total_error_pct / len(critical_data)
    
    if avg_error_pct < best_avg_error:
        best_avg_error = avg_error_pct
        best_mult = mult
        best_base = avg_base

print(f"Best multiplier: {best_mult:.4f}")
print(f"Best base XP: {best_base:.8f}")
print(f"Average error on critical levels: {best_avg_error:.2f}%\n")

# Build table and test
xp_table = {1: 0}
total_xp = 0
for level in range(2, 201):
    total_xp += best_base * (best_mult ** level)
    xp_table[level] = int(total_xp)

print("Predictions for critical players:")
print("-"*70)
for level, actual_xp, name in critical_data:
    pred = xp_table[level]
    for test_level in range(1, 200):
        if xp_table.get(test_level + 1, float('inf')) > actual_xp >= xp_table[test_level]:
            diff = test_level - level
            print(f"{name:15s} L{level} ({actual_xp:>12,} XP) → Predicted L{test_level} ({diff:+d})")
            break

print(f"\nMultiplier: {best_mult:.4f}, Base: {best_base:.8f}")
