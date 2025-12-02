"""
Optimize XP multiplier using comprehensive dataset from both cluster roots
29 known level-to-XP mappings spanning L9 to L143
"""

# Known level -> XP mappings from both cluster roots + Amissa backup
known_data = [
    (9, 877.0596923828125),
    (15, 1141.239990234375),
    (20, 2096.5478515625),
    (21, 2286.783203125),
    (25, 3117.17333984375),
    (39, 9177.9521484375),
    (64, 28090.568359375),
    (68, 39440.0),
    (71, 55484.18359375),
    (74, 95385.7265625),
    (78, 146580.0625),
    (82, 259670.921875),
    (83, 280700.40625),
    (88, 497640.84375),
    (89, 549540.625),  # Anjo from Amissa
    (89, 564968.75),   # Lex XD from Amissa
    (89, 592599.9375), # Anjo from valguero
    (90, 424091.96875), # Cassian from Amissa
    (90, 612400.0),    # Cassian from astraeos
    (95, 975648.9375),
    (96, 1107271.5),
    (97, 1259268.875),
    (114, 6179425.0),
    (117, 7541021.0),
    (131, 2933268.25),  # Jaxxx extinction
    (131, 20947286.0),  # Jaxxx island
    (132, 4391253.5),   # BoldPhoenix patreon
    (134, 51915584.0),
    (143, 142988992.0),
]

print("Known level-to-XP data points:")
print(f"Total data points: {len(known_data)}")
print(f"Level range: {min(l for l, _ in known_data)} to {max(l for l, _ in known_data)}")
print()

# Notice: We have duplicates with different XP values!
# L89: 549K, 564K, 592K
# L90: 424K, 612K
# L131: 2.9M, 20.9M
# L132: 4.3M

# This suggests players might have different amounts of XP at the same level
# Let's use the HIGHEST XP for each level (most conservative)

from collections import defaultdict
level_to_max_xp = defaultdict(float)
for level, xp in known_data:
    level_to_max_xp[level] = max(level_to_max_xp[level], xp)

print("Consolidated to highest XP per level:")
unique_data = sorted([(l, xp) for l, xp in level_to_max_xp.items()])
for level, xp in unique_data:
    print(f"  L{level:3d}: {xp:>15,.2f} XP")
print()

# Calculate XP curve: XP[n] = sum(base_xp * multiplier^i for i in range(2, n+1))
def calculate_xp_for_level(level, multiplier, base_xp):
    """Calculate total XP required for a level using geometric progression."""
    if level <= 1:
        return 0.0
    total_xp = 0.0
    for i in range(2, level + 1):
        total_xp += base_xp * (multiplier ** i)
    return total_xp

def xp_to_level(xp, multiplier, base_xp):
    """Find level from XP using the curve."""
    if xp <= 0:
        return 1
    for level in range(1, 201):
        level_xp = calculate_xp_for_level(level, multiplier, base_xp)
        next_xp = calculate_xp_for_level(level + 1, multiplier, base_xp)
        if level_xp <= xp < next_xp:
            return level
    return 200

# Test different multipliers
print("="*70)
print("Testing multipliers with comprehensive dataset:")
print("="*70)
print()

best_multiplier = None
best_base_xp = None
best_error = float('inf')
best_predictions = []

# Focus on the critical high-level players
critical_levels = [117, 131, 132, 134, 143]

for mult_hundredths in range(1100, 1150):
    multiplier = mult_hundredths / 1000.0
    
    # Calculate average base_xp from multiple reference points
    base_xps = []
    for level, xp in unique_data:
        if level in critical_levels:
            # Solve for base_xp: xp = sum(base_xp * mult^i)
            series_sum = sum(multiplier ** i for i in range(2, level + 1))
            if series_sum > 0:
                base_xp = xp / series_sum
                base_xps.append(base_xp)
    
    if not base_xps:
        continue
    
    avg_base_xp = sum(base_xps) / len(base_xps)
    
    # Test predictions on ALL known data
    predictions = []
    total_error = 0.0
    for level, xp in unique_data:
        predicted_level = xp_to_level(xp, multiplier, avg_base_xp)
        error = abs(predicted_level - level)
        total_error += error
        predictions.append((level, predicted_level, error, xp))
    
    avg_error = total_error / len(unique_data)
    
    # Track best result
    if avg_error < best_error:
        best_error = avg_error
        best_multiplier = multiplier
        best_base_xp = avg_base_xp
        best_predictions = predictions

print(f"\n{'='*70}")
print(f"OPTIMAL RESULT:")
print(f"{'='*70}")
print(f"Best multiplier: {best_multiplier:.4f}")
print(f"Best base XP: {best_base_xp:.8f}")
print(f"Average error across ALL {len(unique_data)} levels: {best_error:.2f} levels")
print()

# Show predictions for all unique levels
print(f"Predictions for all {len(unique_data)} unique levels:")
print(f"{'-'*70}")
print(f"{'Actual':>6} {'Predicted':>9} {'Error':>6} {'XP':>15}")
print(f"{'-'*70}")

for actual_level, predicted_level, error, xp in sorted(best_predictions):
    status = "✓" if error == 0 else "±" if error <= 2 else "✗"
    print(f"L{actual_level:3d} -> L{predicted_level:3d}   {error:+5.1f}   {xp:>15,.0f}  {status}")

# Count accuracy distribution
perfect = len([e for _, _, e, _ in best_predictions if e == 0])
within_1 = len([e for _, _, e, _ in best_predictions if e <= 1])
within_2 = len([e for _, _, e, _ in best_predictions if e <= 2])
within_3 = len([e for _, _, e, _ in best_predictions if e <= 3])

print(f"\n{'-'*70}")
print(f"Accuracy Summary:")
print(f"  Perfect (±0): {perfect}/{len(unique_data)} ({100*perfect/len(unique_data):.1f}%)")
print(f"  Within ±1:    {within_1}/{len(unique_data)} ({100*within_1/len(unique_data):.1f}%)")
print(f"  Within ±2:    {within_2}/{len(unique_data)} ({100*within_2/len(unique_data):.1f}%)")
print(f"  Within ±3:    {within_3}/{len(unique_data)} ({100*within_3/len(unique_data):.1f}%)")

# Generate complete XP table
print(f"\n{'='*70}")
print("Generating complete 200-level XP table...")
print(f"{'='*70}")

xp_table = {}
for level in range(1, 201):
    xp_table[level] = calculate_xp_for_level(level, best_multiplier, best_base_xp)

# Show sample levels
sample_levels = [1, 10, 20, 50, 100, 117, 132, 134, 143, 150, 180, 200]
print("\nSample XP values:")
for level in sample_levels:
    print(f"  Level {level:3d}: {xp_table[level]:>20,.0f} XP")

print(f"\nThis curve is now based on {len(known_data)} data points from {len(unique_data)} unique levels!")
print(f"Average accuracy: ±{best_error:.2f} levels")
