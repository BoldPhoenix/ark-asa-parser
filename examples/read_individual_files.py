"""
Example of reading individual player and tribe files
"""
from ark_asa_parser import ArkSaveReader
from pathlib import Path

def read_player_file():
    """Example of reading a specific player profile file"""
    save_dir = Path("R:/PhoenixArk/asaserver_island/ShooterGame/Saved/SavedArks/TheIsland_WP")
    reader = ArkSaveReader(save_dir)
    
    # Find a player profile file
    profile_files = list(save_dir.glob("*.arkprofile"))
    if not profile_files:
        print("No player profiles found!")
        return
    
    # Read first profile
    profile_path = profile_files[0]
    player = reader.read_profile_file(profile_path)
    
    if player:
        print("Player Profile:")
        print(f"  File: {profile_path.name}")
        print(f"  Player Name: {player.player_name}")
        print(f"  Character Name: {player.character_name}")
        print(f"  EOS ID: {player.eos_id}")
        print(f"  Tribe ID: {player.tribe_id}")
        print(f"  Level: {player.level}")
        print(f"  Experience: {player.experience}")

def read_tribe_file():
    """Example of reading a specific tribe file"""
    save_dir = Path("R:/PhoenixArk/asaserver_island/ShooterGame/Saved/SavedArks/TheIsland_WP")
    reader = ArkSaveReader(save_dir)
    
    # Find a tribe file
    tribe_files = list(save_dir.glob("*.arktribe"))
    if not tribe_files:
        print("No tribe files found!")
        return
    
    # Read first tribe
    tribe_path = tribe_files[0]
    tribe = reader.read_tribe_file(tribe_path)
    
    if tribe:
        print("\nTribe File:")
        print(f"  File: {tribe_path.name}")
        print(f"  Tribe Name: {tribe.tribe_name}")
        print(f"  Tribe ID: {tribe.tribe_id}")
        print(f"  Owner: {tribe.owner_name}")
        print(f"  Member Count: {tribe.member_count}")

def main():
    print("Reading individual save files\n")
    print("=" * 50)
    
    read_player_file()
    print("\n" + "=" * 50)
    read_tribe_file()

if __name__ == "__main__":
    main()
