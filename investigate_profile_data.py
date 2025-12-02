"""
Investigate what progression/achievement data is stored in ARK profile files
Looking for: explorer notes, boss kills, ascensions, level boosts
"""

from pathlib import Path
from ark_asa_parser import ArkProfile

# Find a sample profile (they use Steam IDs as filenames)
amissa_path = Path(r"X:\Amissa\Amissa")
island_path = Path(r"R:\PhoenixArk\asaserver_island\ShooterGame\Saved\SavedArks")

profile_path = None
if amissa_path.exists():
    profiles = list(amissa_path.glob("*.arkprofile"))
    if profiles:
        profile_path = profiles[0]
elif island_path.exists():
    profiles = list(island_path.glob("*.arkprofile"))
    if profiles:
        profile_path = profiles[0]

if not profile_path:
    print("❌ No profile files found!")
    exit(1)

print(f"Loading profile: {profile_path.name}")
print("="*80)

profile = ArkProfile(profile_path)

print("\n1. BASIC PLAYER INFO:")
print("-"*80)
print(f"Name: {profile.character.character_name if hasattr(profile.character, 'character_name') else 'N/A'}")
print(f"Experience: {profile.character.experience if hasattr(profile.character, 'experience') else 'N/A'}")

print("\n2. ALL AVAILABLE PROPERTIES:")
print("-"*80)
print("Searching for progression/achievement related properties...")

# Get all properties from the character
char_dict = vars(profile.character) if hasattr(profile, 'character') else {}

interesting_keywords = [
    'explorer', 'note', 'boss', 'ascen', 'achievement', 'unlock',
    'discover', 'level', 'boost', 'bonus', 'reward', 'progression',
    'complete', 'finish', 'defeat', 'kill', 'dossier'
]

print("\nProperties containing progression keywords:")
found_any = False
for key, value in char_dict.items():
    key_lower = str(key).lower()
    if any(keyword in key_lower for keyword in interesting_keywords):
        print(f"  {key}: {value}")
        found_any = True

if not found_any:
    print("  No obvious progression properties found")

print("\n3. ALL PROPERTIES (full dump):")
print("-"*80)
for key, value in sorted(char_dict.items()):
    # Truncate long values
    str_value = str(value)
    if len(str_value) > 100:
        str_value = str_value[:100] + "..."
    print(f"  {key}: {str_value}")

print("\n4. CHECKING RAW PROFILE DATA:")
print("-"*80)

# Try to access raw profile data
try:
    with open(profile_path, 'rb') as f:
        data = f.read()
    
    # Search for specific strings in binary data
    search_terms = [
        b'ExplorerNote',
        b'Boss',
        b'Ascension',
        b'Achievement',
        b'Dossier',
        b'LevelUp',
        b'Experience',
    ]
    
    print("Searching for strings in binary profile data:")
    for term in search_terms:
        count = data.count(term)
        if count > 0:
            print(f"  Found '{term.decode()}': {count} occurrences")
    
except Exception as e:
    print(f"Error reading raw profile: {e}")

print("\n5. RCON COMMANDS:")
print("-"*80)
print("RCON commands that might help:")
print("  GetPlayerIDForSteamID <steamid>     - Get player's internal ID")
print("  GetPlayerData <playerid>            - Not available in ASA")
print("  ListPlayers                         - Shows online players only")
print()
print("⚠️  RCON typically doesn't expose explorer notes/boss completion data")
print("    This data is usually stored in the profile files or tribe logs")

print("\n6. ALTERNATIVE APPROACHES:")
print("-"*80)
print("Possible ways to get level boost data:")
print()
print("  A) Parse tribe logs (if available)")
print("     - Logs might contain 'Player X discovered explorer note'")
print("     - Logs might contain 'Tribe defeated Boss Y'")
print()
print("  B) Track level changes over time")
print("     - Run collect_player_data.py daily")
print("     - If level increases without proportional XP gain → level boost")
print("     - Example: Player goes L100→L105 but XP only increased 100K")
print()
print("  C) Compare same player across multiple servers")
print("     - If same player has different level/XP ratios → boosts used")
print("     - We already see this: Jaxxx L131 has 20.9M on Island vs 2.9M on Extinction")
print()
print("  D) Community data collection")
print("     - Ask players to report: 'I'm level X with Y explorer notes collected'")
print("     - Build database of notes→levels mapping")
print()
print("  E) Reverse engineer from 'pure grind' players")
print("     - Find players who NEVER leave their home server")
print("     - Assume they didn't get notes (or got same notes as others)")
print("     - Use their data as baseline")

print("\n" + "="*80)
print("CONCLUSION:")
print("="*80)
print("ARK profile files likely don't expose explorer note/boss completion counts")
print("directly in easily parseable properties. Best approach:")
print()
print("1. Use MAXIMUM XP per level as 'pure grind' baseline")
print("2. Track players over time to detect level boosts")
print("3. Flag players with 'boosted' status when level >> expected for XP")
print("4. Continuously refine curve using high-XP players (pure grinders)")
