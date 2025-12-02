"""
Analyze data quality - find inconsistencies in level-to-XP mappings
"""

known_data = [
    (9, 877.0596923828125, "Rhyno", "PhoenixArk/island"),
    (15, 1141.239990234375, "Tester", "PhoenixArk/island"),
    (20, 2096.5478515625, "Ami Fallen", "Amissa_backup"),
    (21, 2286.783203125, "Tapeworm", "Amissa_backup"),
    (25, 3117.17333984375, "LionsLord", "PhoenixArk/island"),
    (39, 9177.9521484375, "Eos", "Amissa_backup"),
    (64, 28090.568359375, "Aatxe", "PhoenixArk/island"),
    (68, 39440.0, "Sevey", "Amissa_backup"),
    (71, 55484.18359375, "Dc kid", "PhoenixArk/island"),
    (74, 95385.7265625, "Robf73", "Amissa_backup"),
    (78, 146580.0625, "Raven Yuri", "PhoenixArk/island"),
    (82, 259670.921875, "Reina", "PhoenixArk/island"),
    (83, 280700.40625, "ShadiDK", "Amissa_backup"),
    (88, 497640.84375, "Poli", "PhoenixArk/island"),
    (89, 549540.625, "Anjo", "Amissa_backup"),
    (89, 564968.75, "Lex XD", "Amissa_backup"),
    (89, 592599.9375, "Anjo", "PhoenixArk/valguero"),
    (90, 424091.96875, "Cassian", "Amissa_backup"),
    (90, 612400.0, "Cassian", "PhoenixArk/astraeos"),
    (95, 975648.9375, "Sex4TRex", "PhoenixArk/astraeos"),
    (96, 1107271.5, "Mathias", "Amissa_backup"),
    (97, 1259268.875, "Jake", "PhoenixArk/island"),
    (114, 6179425.0, "Joker", "PhoenixArk/astraeos"),
    (117, 7541021.0, "Panther", "PhoenixArk/astraeos"),
    (131, 2933268.25, "Jaxxx", "PhoenixArk/extinction"),
    (131, 20947286.0, "Jaxxx", "PhoenixArk/island"),  # Same player, HUGE difference!
    (132, 4391253.5, "BoldPhoenix", "ark/patreon"),
    (134, 51915584.0, "LadySif", "Amissa_backup"),
    (143, 142988992.0, "Axl", "Amissa_backup"),
]

print("="*80)
print("DATA QUALITY ANALYSIS")
print("="*80)
print()

# Sort by level then XP
sorted_data = sorted(known_data, key=lambda x: (x[0], x[1]))

print("All data points (sorted by level, then XP):")
print("-"*80)
for level, xp, name, server in sorted_data:
    print(f"L{level:3d}: {xp:>15,.0f} XP | {name:20s} | {server}")
print()

# Find anomalies: where a lower level has more XP than a higher level
print("="*80)
print("ANOMALIES DETECTED:")
print("="*80)
print()

anomalies = []
for i in range(len(sorted_data) - 1):
    level1, xp1, name1, server1 = sorted_data[i]
    for j in range(i + 1, len(sorted_data)):
        level2, xp2, name2, server2 = sorted_data[j]
        if level1 < level2 and xp1 > xp2:
            anomalies.append((level1, xp1, name1, server1, level2, xp2, name2, server2))
            print(f"⚠️  L{level1} ({name1:15s}) has {xp1:>15,.0f} XP")
            print(f"    L{level2} ({name2:15s}) has {xp2:>15,.0f} XP  ← LOWER!")
            print(f"    Difference: {xp1 - xp2:,.0f} XP")
            print(f"    Servers: {server1} vs {server2}")
            print()

if not anomalies:
    print("No anomalies found! Data is consistent.")
else:
    print(f"Found {len(anomalies)} anomalies!")
    print()
    print("="*80)
    print("HYPOTHESIS: Different servers might have different XP multipliers!")
    print("="*80)
    print()
    
    # Group by server to see if there's a pattern
    from collections import defaultdict
    server_data = defaultdict(list)
    for level, xp, name, server in sorted_data:
        server_data[server].append((level, xp, name))
    
    print("Data grouped by server:")
    print("-"*80)
    for server in sorted(server_data.keys()):
        print(f"\n{server}:")
        for level, xp, name in sorted(server_data[server]):
            print(f"  L{level:3d}: {xp:>15,.0f} XP | {name}")

print()
print("="*80)
print("CONCLUSION:")
print("="*80)
print()

# The major inconsistency
print("Major issue detected:")
print(f"  Jaxxx L131 on PhoenixArk/island:    20,947,286 XP")
print(f"  Jaxxx L131 on PhoenixArk/extinction: 2,933,268 XP")
print(f"  BoldPhoenix L132 on ark/patreon:     4,391,254 XP")
print()
print("This suggests ONE of these is incorrect:")
print("  1. The level reading from the profile might be wrong")
print("  2. The XP reading from the profile might be wrong")
print("  3. Different servers use different XP multipliers")
print("  4. The profile data got corrupted/desynced")
print()
print("Since L131 Island has 20.9M XP and L134 Amissa has 51.9M XP,")
print("the Island data point seems more consistent with high-level progression.")
print()
print("RECOMMENDATION: Use only the data from servers that show consistent progression.")
print("Focus on: PhoenixArk/island, PhoenixArk/astraeos, Amissa_backup")
