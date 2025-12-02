"""Search for dino data in world save"""
import sqlite3
from pathlib import Path

world_path = Path(r"R:\PhoenixArk\asaserver_aberration\ShooterGame\Saved\SavedArks\Aberration_WP\Aberration_WP.ark")

conn = sqlite3.connect(str(world_path))
cursor = conn.cursor()

# Get all entries from game table
cursor.execute("SELECT key, value FROM game LIMIT 1000")
rows = cursor.fetchall()

print(f"Analyzing {len(rows)} rows from game table\n")

# Look for dino class names in values
dino_terms = [
    b"Dino_Character",
    b"DinoCharacter",
    b"Tamed",
    b"TameIneffectivenessModifier",
    b"DinoID",
    b"TamerString",
    b"TargetingTeam",
    b"TribeName",
    b"bIsTamed",
    b"BaseLevelCount",
    b"ExtraCharacterLevel"
]

matches = {}
for term in dino_terms:
    count = 0
    sample_key = None
    for key, value in rows:
        if term in value:
            count += 1
            if sample_key is None:
                sample_key = key
    if count > 0:
        matches[term.decode('ascii')] = (count, sample_key)

print("Dino-related terms found:")
for term, (count, key) in sorted(matches.items(), key=lambda x: x[1][0], reverse=True):
    print(f"  {term:30s}: {count:4d} occurrences")
    if key:
        print(f"    Sample key: {key.hex()[:40]}...")

# Check for class names with "_C" suffix (typical for UE5 classes)
print("\nLooking for Dino class patterns...")
class_count = 0
for key, value in rows:
    if b"_Character_BP_" in value and b"_C" in value:
        class_count += 1
        if class_count <= 3:
            # Try to extract class name
            try:
                idx = value.find(b"_Character_BP_")
                if idx != -1:
                    # Look backward for start of string
                    start = max(0, idx - 50)
                    chunk = value[start:idx+50]
                    print(f"  Found class pattern: {chunk[:80]}")
            except:
                pass

print(f"\nTotal entries with dino class patterns: {class_count}")

conn.close()