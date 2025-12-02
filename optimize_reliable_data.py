"""
Optimize XP curve using ONLY reliable data (servers with consistent progression)
Excludes: ark/patreon, PhoenixArk/extinction (data inconsistencies detected)
"""

# Reliable data ONLY from: PhoenixArk/island, PhoenixArk/astraeos, Amissa_backup, PhoenixArk/valguero
reliable_data = [
    # PhoenixArk/island (most data points)
    (9, 877.0596923828125, "Rhyno"),
    (15, 1141.239990234375, "Tester"),
    (25, 3117.17333984375, "LionsLord"),
    (64, 28090.568359375, "Aatxe"),
    (71, 55484.18359375, "Dc kid"),
    (78, 146580.0625, "Raven Yuri"),
    (82, 259670.921875, "Reina"),
    (88, 497640.84375, "Poli"),
    (97, 1259268.875, "Jake"),
    (131, 20947286.0, "Jaxxx"),  # High-level reference!
    
    # PhoenixArk/astraeos
    (90, 612400.0, "Cassian"),
    (95, 975648.9375, "Sex4TRex"),
    (114, 6179425.0, "Joker"),
    (117, 7541021.0, "Panther"),
    
    # Amissa_backup (includes highest levels!)
    (20, 2096.5478515625, "Ami Fallen"),
    (21, 2286.783203125, "Tapeworm"),
    (39, 9177.9521484375, "Eos"),
    (68, 39440.0, "Sevey"),
    (74, 95385.7265625, "Robf73"),
    (83, 280700.40625, "ShadiDK"),
    (89, 592599.9375, "Anjo"),  # Use highest value
    (96, 1107271.5, "Mathias"),
    (134, 51915584.0, "LadySif"),  # Critical high-level!
    (143, 142988992.0, "Axl"),  # Highest level!
    
    # PhoenixArk/valguero
    # (89, 592599.9375, "Anjo"),  # Already included above
]

print("="*70)
print("RELIABLE DATA ONLY (24 data points)")
print("="*70)
print()

for level, xp, name in sorted(reliable_data):
    print(f"L{level:3d}: {xp:>15,.2f} XP | {name:20s}")
print()

# Calculate XP curve
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
print("Optimizing with reliable data only...")
print("="*70)
print()

best_multiplier = None
best_base_xp = None
best_error = float('inf')
best_predictions = []

# Critical high-level players for base_xp calculation
critical_levels = [117, 131, 134, 143]

for mult_hundredths in range(1100, 1200):
    multiplier = mult_hundredths / 1000.0
    
    # Calculate average base_xp from high-level players
    base_xps = []
    for level, xp, name in reliable_data:
        if level in critical_levels:
            series_sum = sum(multiplier ** i for i in range(2, level + 1))
            if series_sum > 0:
                base_xp = xp / series_sum
                base_xps.append(base_xp)
    
    if not base_xps:
        continue
    
    avg_base_xp = sum(base_xps) / len(base_xps)
    
    # Test predictions
    predictions = []
    total_error = 0.0
    for level, xp, name in reliable_data:
        predicted_level = xp_to_level(xp, multiplier, avg_base_xp)
        error = abs(predicted_level - level)
        total_error += error
        predictions.append((level, predicted_level, error, xp, name))
    
    avg_error = total_error / len(reliable_data)
    
    # Track best result
    if avg_error < best_error:
        best_error = avg_error
        best_multiplier = multiplier
        best_base_xp = avg_base_xp
        best_predictions = predictions

print(f"\n{'='*70}")
print(f"OPTIMAL RESULT WITH RELIABLE DATA:")
print(f"{'='*70}")
print(f"Best multiplier: {best_multiplier:.4f}")
print(f"Best base XP: {best_base_xp:.8f}")
print(f"Average error across {len(reliable_data)} levels: {best_error:.2f} levels")
print()

# Show all predictions
print(f"All predictions:")
print(f"{'-'*70}")
print(f"{'Actual':>6} {'Predicted':>9} {'Error':>6} {'XP':>15} {'Name'}")
print(f"{'-'*70}")

for actual_level, predicted_level, error, xp, name in sorted(best_predictions):
    status = "✓" if error == 0 else "±" if error <= 2 else "✗"
    print(f"L{actual_level:3d} -> L{predicted_level:3d}   {error:+5.1f}   {xp:>15,.0f}  {name:20s} {status}")

# Accuracy summary
perfect = len([e for _, _, e, _, _ in best_predictions if e == 0])
within_1 = len([e for _, _, e, _, _ in best_predictions if e <= 1])
within_2 = len([e for _, _, e, _, _ in best_predictions if e <= 2])
within_3 = len([e for _, _, e, _, _ in best_predictions if e <= 3])

print(f"\n{'-'*70}")
print(f"Accuracy Summary:")
print(f"  Perfect (±0): {perfect}/{len(reliable_data)} ({100*perfect/len(reliable_data):.1f}%)")
print(f"  Within ±1:    {within_1}/{len(reliable_data)} ({100*within_1/len(reliable_data):.1f}%)")
print(f"  Within ±2:    {within_2}/{len(reliable_data)} ({100*within_2/len(reliable_data):.1f}%)")
print(f"  Within ±3:    {within_3}/{len(reliable_data)} ({100*within_3/len(reliable_data):.1f}%)")

# Show critical high-level predictions
print(f"\n{'-'*70}")
print("Critical High-Level Players:")
print(f"{'-'*70}")
for actual_level, predicted_level, error, xp, name in best_predictions:
    if actual_level >= 110:
        print(f"  {name:15s} L{actual_level:3d} → Predicted L{predicted_level:3d} ({error:+.0f})")

# Generate XP table
print(f"\n{'='*70}")
print("Sample XP values from optimized curve:")
print(f"{'='*70}")

sample_levels = [1, 10, 20, 50, 100, 117, 131, 132, 134, 143, 150, 180, 200]
for level in sample_levels:
    xp_val = calculate_xp_for_level(level, best_multiplier, best_base_xp)
    print(f"  Level {level:3d}: {xp_val:>20,.0f} XP")

print(f"\nThis curve is based on {len(reliable_data)} reliable data points from vanilla servers!")
print(f"Average accuracy: ±{best_error:.2f} levels")
