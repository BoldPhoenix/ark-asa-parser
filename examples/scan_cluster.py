"""
Example of scanning all servers in a cluster
"""
from ark_asa_parser import scan_all_servers
from pathlib import Path

def main():
    # Path to cluster directory containing multiple servers
    cluster_path = Path("R:/PhoenixArk")
    
    print(f"Scanning cluster: {cluster_path}\n")
    
    # Scan all servers
    servers = scan_all_servers(cluster_path)
    
    if not servers:
        print("No servers found!")
        return
    
    print(f"Found {len(servers)} servers\n")
    print("=" * 80)
    
    # Iterate through all servers
    for server_name, reader in sorted(servers.items()):
        print(f"\nSERVER: {server_name.upper()}")
        print("-" * 80)
        
        # Get database info
        info = reader.get_database_info()
        size_mb = info.get('file_size', 0) / (1024 * 1024)
        
        # Get players and tribes
        players = reader.get_all_players()
        tribes = reader.get_all_tribes()
        
        print(f"Save Size: {size_mb:.2f} MB")
        print(f"Last Modified: {info.get('file_modified', 'Unknown')}")
        print(f"Players: {len(players)}")
        print(f"Tribes: {len(tribes)}")
        
        # Show player names if any
        if players:
            print("\nActive Players:")
            for player in players[:5]:  # Show first 5
                print(f"  - {player.player_name} ({player.character_name})")
            if len(players) > 5:
                print(f"  ... and {len(players) - 5} more")
        
        # Show tribe names if any
        if tribes:
            print("\nActive Tribes:")
            for tribe in tribes[:5]:  # Show first 5
                print(f"  - {tribe.tribe_name} ({tribe.member_count} members)")
            if len(tribes) > 5:
                print(f"  ... and {len(tribes) - 5} more")
    
    print("\n" + "=" * 80)
    
    # Summary statistics
    total_players = sum(len(reader.get_all_players()) for reader in servers.values())
    total_tribes = sum(len(reader.get_all_tribes()) for reader in servers.values())
    
    print(f"\nCLUSTER SUMMARY")
    print(f"Total Servers: {len(servers)}")
    print(f"Total Players: {total_players}")
    print(f"Total Tribes: {total_tribes}")

if __name__ == "__main__":
    main()
