"""
Comprehensive XP curve optimization with ALL collected data
Including: Original 24 + Extinction 6 = 30 unique level data points
"""

# ALL collected data (using MAX XP per level for pure grind baseline)
all_known_data = [
    # Original PhoenixArk Island
    (9, 877.0596923828125, "Rhyno", "PhoenixArk/island"),
    (15, 1141.239990234375, "Tester", "PhoenixArk/island"),
    (25, 3117.17333984375, "LionsLord", "PhoenixArk/island"),
    (64, 28090.568359375, "Aatxe", "PhoenixArk/island"),
    (71, 55484.18359375, "Dc kid", "PhoenixArk/island"),
    (78, 146580.0625, "Raven Yuri", "PhoenixArk/island"),
    (82, 259670.921875, "Reina", "PhoenixArk/island"),
    (88, 497640.84375, "Poli", "PhoenixArk/island"),
    (97, 1259268.875, "Jake", "PhoenixArk/island"),
    (131, 20947286.0, "Jaxxx", "PhoenixArk/island"),
    
    # PhoenixArk Astraeos
    (90, 612400.0, "Cassian", "PhoenixArk/astraeos"),
    (95, 975648.9375, "Sex4TRex", "PhoenixArk/astraeos"),
    (114, 6179425.0, "Joker", "PhoenixArk/astraeos"),
    (117, 7541021.0, "Panther", "PhoenixArk/astraeos"),
    
    # Amissa backup
    (20, 2096.5478515625, "Ami Fallen", "Amissa"),
    (21, 2286.783203125, "Tapeworm", "Amissa"),
    (39, 9177.9521484375, "Eos", "Amissa"),
    (68, 39440.0, "Sevey", "Amissa"),
    (74, 95385.7265625, "Robf73", "Amissa"),
    (83, 280700.40625, "ShadiDK", "Amissa"),
    (89, 592599.9375, "Anjo", "Amissa/valguero"),  # MAX of 3 L89 values
    (96, 1107271.5, "Mathias", "Amissa"),
    (134, 51915584.0, "LadySif", "Amissa"),  # PURE GRIND (higher than Sunniva)
    (143, 142988992.0, "Axl", "Amissa"),
    
    # NEW: Extinction backup (X:\)
    (88, 459138.0, "Human", "Extinction"),  # LOWER than Poli's 497K - likely boosted
    (105, 4098538.0, "Buzz", "Extinction"),  # MAX of 3 L105 values
    # Note: Sunniva L134 = 43.6M is LOWER than LadySif's 51.9M, so we keep LadySif as baseline
]

print("="*80)
print("COMPREHENSIVE XP CURVE OPTIMIZATION")
print("="*80)
print()

# Group by level, keep MAX XP (pure grind)
from collections import defaultdict
level_max_xp = defaultdict(lambda: (0, None, None))

for level, xp, name, location in all_known_data:
    if xp > level_max_xp[level][0]:
        level_max_xp[level] = (xp, name, location)

pure_grind_data = sorted([(level, xp, name, location) for level, (xp, name, location) in level_max_xp.items()])

print(f"Pure Grind Baseline: {len(pure_grind_data)} unique levels")
print("-"*80)
for level, xp, name, location in pure_grind_data:
    # Show if there were other (boosted) values for this level
    alternates = [(x, n, l) for lv, x, n, l in all_known_data if lv == level and x < xp]
    boost_note = f"  (vs {len(alternates)} boosted)" if alternates else ""
    print(f"L{level:3d}: {xp:>15,.0f} XP | {name:20s} | {location:20s}{boost_note}")

print()

# Calculate XP curve
def calculate_xp_for_level(level, multiplier, base_xp):
    if level <= 1:
        return 0.0
    return sum(base_xp * (multiplier ** i) for i in range(2, level + 1))

def xp_to_level(xp, multiplier, base_xp):
    if xp <= 0:
        return 1
    for level in range(1, 201):
        level_xp = calculate_xp_for_level(level, multiplier, base_xp)
        next_xp = calculate_xp_for_level(level + 1, multiplier, base_xp)
        if level_xp <= xp < next_xp:
            return level
    return 200

# Optimize
print("="*80)
print("Optimizing multiplier with expanded dataset...")
print("="*80)
print()

best_multiplier = None
best_base_xp = None
best_error = float('inf')
best_predictions = []

critical_levels = [114, 117, 131, 134, 143]

for mult_hundredths in range(1090, 1200):
    multiplier = mult_hundredths / 1000.0
    
    # Calculate base_xp from high-level pure grind data
    base_xps = []
    for level, xp, name, location in pure_grind_data:
        if level in critical_levels:
            series_sum = sum(multiplier ** i for i in range(2, level + 1))
            if series_sum > 0:
                base_xps.append(xp / series_sum)
    
    if not base_xps:
        continue
    
    avg_base_xp = sum(base_xps) / len(base_xps)
    
    # Test predictions with WEIGHTED error (high levels count more)
    predictions = []
    total_weighted_error = 0.0
    
    for level, xp, name, location in pure_grind_data:
        predicted_level = xp_to_level(xp, multiplier, avg_base_xp)
        error = abs(predicted_level - level)
        weight = 1.0 if level < 100 else 3.0  # High levels weighted 3x
        
        total_weighted_error += error * weight
        predictions.append((level, predicted_level, error, xp, name))
    
    # Calculate weighted average error
    total_weight = sum(1.0 if l < 100 else 3.0 for l, _, _, _ in pure_grind_data)
    avg_weighted_error = total_weighted_error / total_weight
    
    if avg_weighted_error < best_error:
        best_error = avg_weighted_error
        best_multiplier = multiplier
        best_base_xp = avg_base_xp
        best_predictions = predictions

print(f"OPTIMAL RESULT:")
print(f"{'='*80}")
print(f"Multiplier: {best_multiplier:.4f}")
print(f"Base XP:    {best_base_xp:.8f}")
print(f"Weighted avg error: {best_error:.2f} levels (high levels weighted 3x)")
print(f"Dataset: {len(all_known_data)} total data points, {len(pure_grind_data)} unique levels")
print()

# Show predictions
print("Predictions for Pure Grind Baseline:")
print("-"*80)
print(f"{'Actual':>6} {'Predicted':>9} {'Error':>6} {'XP':>15} {'Player'}")
print("-"*80)

for actual_level, predicted_level, error, xp, name in sorted(best_predictions):
    status = "✓" if error == 0 else "±" if error <= 2 else "✗"
    print(f"L{actual_level:3d} -> L{predicted_level:3d}   {error:+5.1f}   {xp:>15,.0f}  {name:20s} {status}")

# Accuracy stats
perfect = sum(1 for _, _, e, _, _ in best_predictions if e == 0)
within_1 = sum(1 for _, _, e, _, _ in best_predictions if e <= 1)
within_2 = sum(1 for _, _, e, _, _ in best_predictions if e <= 2)
within_3 = sum(1 for _, _, e, _, _ in best_predictions if e <= 3)

print(f"\n{'-'*80}")
print(f"Accuracy Summary:")
print(f"  Perfect (±0): {perfect}/{len(pure_grind_data)} ({100*perfect/len(pure_grind_data):.1f}%)")
print(f"  Within ±1:    {within_1}/{len(pure_grind_data)} ({100*within_1/len(pure_grind_data):.1f}%)")
print(f"  Within ±2:    {within_2}/{len(pure_grind_data)} ({100*within_2/len(pure_grind_data):.1f}%)")
print(f"  Within ±3:    {within_3}/{len(pure_grind_data)} ({100*within_3/len(pure_grind_data):.1f}%)")

# Show high-level predictions
print(f"\n{'-'*80}")
print("Critical High-Level Players (Pure Grind):")
print(f"{'-'*80}")
for actual_level, predicted_level, error, xp, name in best_predictions:
    if actual_level >= 110:
        print(f"  {name:20s} L{actual_level:3d} → L{predicted_level:3d} ({error:+.0f})")

# Generate final XP table
print(f"\n{'='*80}")
print("Generating Final XP Table for Analytics Dashboard...")
print(f"{'='*80}")

xp_table = {level: int(calculate_xp_for_level(level, best_multiplier, best_base_xp)) for level in range(1, 201)}

sample_levels = [1, 10, 20, 50, 100, 105, 114, 117, 131, 134, 143, 150, 180, 200]
print("\nSample XP values:")
for level in sample_levels:
    print(f"  Level {level:3d}: {xp_table[level]:>20,} XP")

print(f"\n{'='*80}")
print(f"FINAL STATISTICS:")
print(f"{'='*80}")
print(f"Total data points collected: {len(all_known_data)}")
print(f"Unique levels (pure grind baseline): {len(pure_grind_data)}")
print(f"Level range: L{min(l for l, _, _, _ in pure_grind_data)} to L{max(l for l, _, _, _ in pure_grind_data)}")
print(f"Optimal multiplier: {best_multiplier:.4f}")
print(f"Weighted average error: ±{best_error:.2f} levels")
print(f"{'='*80}")
