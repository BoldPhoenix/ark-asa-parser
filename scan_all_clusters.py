"""
Extract player data from BOTH cluster roots: R:\PhoenixArk and R:\ark
Plus Amissa backup from X: drive
"""

from pathlib import Path
from ark_asa_parser import scan_all_servers, ArkSaveReader

print("Scanning multiple cluster roots for comprehensive data...")
print("="*70)

all_players = []

# Scan R:\PhoenixArk
print("\n1. Scanning R:\\PhoenixArk...")
try:
    servers1 = scan_all_servers(Path(r"R:\PhoenixArk"))
    for server_name, reader in servers1.items():
        players = reader.get_all_players()
        for p in players:
            if hasattr(p, 'experience') and hasattr(p, 'character_name'):
                xp = p.experience
                name = p.character_name
                if xp > 500 and name:
                    all_players.append((name, xp, f"PhoenixArk/{server_name}"))
        print(f"  {server_name:15s}: {len(players)} players")
    print(f"  Total from PhoenixArk: {len([p for p in all_players if 'PhoenixArk' in p[2]])} players")
except Exception as e:
    print(f"  Error: {e}")

# Scan R:\ark
print("\n2. Scanning R:\\ark...")
try:
    servers2 = scan_all_servers(Path(r"R:\ark"))
    count_before = len(all_players)
    for server_name, reader in servers2.items():
        players = reader.get_all_players()
        for p in players:
            if hasattr(p, 'experience') and hasattr(p, 'character_name'):
                xp = p.experience
                name = p.character_name
                if xp > 500 and name:
                    all_players.append((name, xp, f"ark/{server_name}"))
        print(f"  {server_name:15s}: {len(players)} players")
    print(f"  Total from ark: {len(all_players) - count_before} players")
except Exception as e:
    print(f"  Error: {e}")

# Scan X:\Amissa backup
print("\n3. Scanning X:\\Amissa backup...")
try:
    amissa_reader = ArkSaveReader(Path(r'X:\Amissa\Amissa'))
    amissa_players = amissa_reader.get_all_players()
    count_before = len(all_players)
    for p in amissa_players:
        if hasattr(p, 'experience') and hasattr(p, 'character_name'):
            xp = p.experience
            name = p.character_name
            if xp > 500 and name:
                all_players.append((name, xp, "Amissa_backup"))
    print(f"  Total from Amissa: {len(all_players) - count_before} players")
except Exception as e:
    print(f"  Error: {e}")

print("\n" + "="*70)
print(f"\nTotal players collected: {len(all_players)}")

# Get unique XP values to understand the distribution
unique_xp = sorted(set(xp for name, xp, server in all_players))
print(f"Unique XP values: {len(unique_xp)}")
print(f"XP range: {unique_xp[0]:,} to {unique_xp[-1]:,}")

# Show XP distribution
print(f"\nXP Distribution:")
print("-"*70)
xp_ranges = [
    (0, 10000, "Low level (0-10K)"),
    (10001, 100000, "Mid level (10K-100K)"),
    (100001, 1000000, "High level (100K-1M)"),
    (1000001, 10000000, "Very high (1M-10M)"),
    (10000001, 100000000, "Ultra high (10M-100M)"),
    (100000001, 1000000000, "Max level (100M+)"),
]

for low, high, label in xp_ranges:
    count = len([xp for name, xp, server in all_players if low <= xp <= high])
    if count > 0:
        print(f"  {label:25s}: {count:4d} players")

# Top players by XP
print(f"\nTop 30 players by XP (potential high levels):")
print("-"*70)
all_players.sort(key=lambda x: x[1], reverse=True)
for i, (name, xp, server) in enumerate(all_players[:30], 1):
    print(f"{i:2d}. {name:20s} {xp:>13,} XP | {server}")

# Known levels from screenshots
known_levels = {
    "Axl": 143, "LadySif": 134, "BoldPhoenix": 132, "Jaxxx": 131,
    "Panther": 117, "Joker": 114, "Mathias": 96, "Jake": 97,
    "Sex4TRex": 95, "Cassian": 90, "Anjo": 89, "Lex XD": 89,
    "Poli": 88, "ShadiDK": 83, "Reina": 82, "Raven Yuri": 78,
    "Robf73": 74, "Koco": 71, "Dc kid": 71, "Sevey": 68,
    "Aatxe": 64, "Eos": 39, "LionsLord": 25, "Tapeworm": 21,
    "Ami Fallen": 20, "Tester": 15, "Rhyno": 9,
}

print(f"\n" + "="*70)
print(f"\nMatching known levels from screenshots:")
print("-"*70)

matched = []
for name, xp, server in all_players:
    if name in known_levels:
        level = known_levels[name]
        matched.append((level, xp, name, server))
        print(f"✓ {name:20s} L{level:3d} = {xp:>13,} XP | {server}")

matched.sort()

print(f"\n✓ Successfully matched {len(matched)}/{len(known_levels)} known players")

# Save comprehensive dataset
with open("comprehensive_player_data.txt", "w", encoding="utf-8") as f:
    f.write(f"# Comprehensive player data from multiple cluster roots\n")
    f.write(f"# Total players: {len(all_players)}\n")
    f.write(f"# Matched with known levels: {len(matched)}\n\n")
    f.write("# Known level -> XP mappings\n")
    f.write("known_level_xp = [\n")
    for level, xp, name, server in matched:
        f.write(f"    ({level}, {xp}, '{name}', '{server}'),\n")
    f.write("]\n\n")
    f.write("# All players (name, xp, server)\n")
    f.write("all_players = [\n")
    for name, xp, server in all_players[:100]:  # First 100
        f.write(f"    ('{name}', {xp}, '{server}'),\n")
    f.write("    # ... truncated\n")
    f.write("]\n")

print(f"\nData saved to: comprehensive_player_data.txt")
print(f"\nWe now have {len(all_players)} total players to analyze!")
