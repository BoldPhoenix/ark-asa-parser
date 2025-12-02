"""
Basic example of reading player and tribe data from ARK saves
"""
from ark_asa_parser import ArkSaveReader
from pathlib import Path

def main():
    # Path to your ARK save directory
    # Adjust this to point to your server's save location
    save_dir = Path("R:/PhoenixArk/asaserver_island/ShooterGame/Saved/SavedArks/TheIsland_WP")
    
    # Create reader
    reader = ArkSaveReader(save_dir)
    
    # Check if save directory is valid
    if not reader.is_valid():
        print(f"Invalid save directory: {save_dir}")
        return
    
    print(f"Reading save data from: {save_dir.name}\n")
    
    # Get database info
    info = reader.get_database_info()
    print(f"Save file size: {info.get('file_size', 0) / (1024*1024):.2f} MB")
    print(f"Last modified: {info.get('file_modified', 'Unknown')}")
    print(f"Tables: {list(info.get('tables', {}).keys())}\n")
    
    # Get all players
    print("=" * 50)
    print("PLAYERS")
    print("=" * 50)
    
    players = reader.get_all_players()
    print(f"Total players: {len(players)}\n")
    
    for player in players:
        print(f"Player: {player.player_name}")
        print(f"  Character: {player.character_name}")
        print(f"  EOS ID: {player.eos_id}")
        print(f"  Tribe ID: {player.tribe_id}")
        print(f"  Level: {player.level}")
        print(f"  Experience: {player.experience}")
        print()
    
    # Get all tribes
    print("=" * 50)
    print("TRIBES")
    print("=" * 50)
    
    tribes = reader.get_all_tribes()
    print(f"Total tribes: {len(tribes)}\n")
    
    for tribe in tribes:
        print(f"Tribe: {tribe.tribe_name}")
        print(f"  ID: {tribe.tribe_id}")
        print(f"  Owner: {tribe.owner_name}")
        print(f"  Members: {tribe.member_count}")
        print()

if __name__ == "__main__":
    main()
