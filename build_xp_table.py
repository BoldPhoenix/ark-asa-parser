"""
Build a complete XP table for ARK ASA using the discovered multiplier.

Using: Multiplier = 1.159, BaseXP = 0.01
Formula: Total XP at level N = sum(0.01 * 1.159^i for i in range(2, N+1))
"""

multiplier = 1.159
base_xp = 0.01

print("Building ARK ASA XP Table (levels 1-200)...\n")

# Build XP table
xp_table = {}
total_xp = 0

# Level 1 starts at 0 XP
xp_table[1] = 0

# Calculate XP needed for each level
for level in range(2, 201):
    xp_for_this_level = base_xp * (multiplier ** level)
    total_xp += xp_for_this_level
    xp_table[level] = int(total_xp)

# Show key levels
print("Key XP values:")
print(f"Level 1: {xp_table[1]:,} XP")
print(f"Level 10: {xp_table[10]:,} XP")
print(f"Level 50: {xp_table[50]:,} XP")
print(f"Level 100: {xp_table[100]:,} XP")
print(f"Level 132: {xp_table[132]:,} XP (actual: 28,615,150)")
print(f"Level 133: {xp_table[133]:,} XP (actual: 33,373,538)")
print(f"Level 150: {xp_table[150]:,} XP")
print(f"Level 180: {xp_table[180]:,} XP")
print(f"Level 200: {xp_table[200]:,} XP")

print("\n" + "="*70)

# Test with known values
print("\nValidation with known player data:")
test_xp = 28615150
print(f"\nPlayer with {test_xp:,} XP is at level:")

for level in range(1, 201):
    if level == 200 or xp_table[level + 1] > test_xp:
        print(f"  Level {level} (table says {xp_table[level]:,} XP)")
        print(f"  Difference: {abs(test_xp - xp_table[level]):,} XP")
        break

# Create Python dictionary format for easy copy-paste
print("\n" + "="*70)
print("\nPython dictionary (first 50 levels):\n")
print("ARK_ASA_XP_TABLE = {")
for level in range(1, 51):
    print(f"    {level}: {xp_table[level]},")
print("    # ... truncated for display")
print("}")

# Save to file
with open("ark_asa_xp_table.txt", "w") as f:
    f.write("ARK_ASA_XP_TABLE = {\n")
    for level in range(1, 201):
        f.write(f"    {level}: {xp_table[level]},\n")
    f.write("}\n")

print("\nFull table saved to: ark_asa_xp_table.txt")

# Create a level lookup function
print("\n" + "="*70)
print("\nLevel lookup function:\n")
print("""
def get_level_from_xp(xp: float, xp_table: dict) -> int:
    \"\"\"Calculate player level from total XP earned.\"\"\"
    if xp <= 0:
        return 1
    
    # Binary search for efficiency
    levels = sorted(xp_table.keys())
    
    for i in range(len(levels) - 1):
        current_level = levels[i]
        next_level = levels[i + 1]
        
        if xp >= xp_table[current_level] and xp < xp_table[next_level]:
            return current_level
    
    # If XP exceeds max level
    return levels[-1]
""")
