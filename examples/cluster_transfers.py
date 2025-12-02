"""
Example usage of cluster transfer reader.

Shows how to scan ClusterObjects folder for transferred items/dinos/characters.
"""
from pathlib import Path
from ark_asa_parser.cluster_reader import (
    scan_cluster_folder,
    get_cluster_summary,
    get_player_cluster_data
)


def example_scan_cluster():
    """Scan ClusterObjects folder and show transfers"""
    # Point to your SavedArks folder
    saved_arks = Path("C:/ASA_Servers/ShooterGame/Saved/SavedArks")
    
    print("=== Scanning Cluster Transfers ===\n")
    
    transfers = scan_cluster_folder(saved_arks)
    
    for transfer_type, transfer_list in transfers.items():
        if transfer_list:
            print(f"\n{transfer_type.upper()}:")
            for t in transfer_list[:5]:  # Show first 5
                print(f"  - {t.file_name}")
                if t.character_name:
                    print(f"    Character: {t.character_name}")
                if t.steam_id:
                    print(f"    Steam ID: {t.steam_id}")
                print(f"    Size: {t.file_size / 1024:.1f} KB")
            
            if len(transfer_list) > 5:
                print(f"  ... and {len(transfer_list) - 5} more")


def example_cluster_summary():
    """Get cluster statistics"""
    saved_arks = Path("C:/ASA_Servers/ShooterGame/Saved/SavedArks")
    
    print("=== Cluster Summary ===\n")
    
    summary = get_cluster_summary(saved_arks)
    
    print(f"Total Files: {summary['total_files']}")
    print(f"Total Size: {summary['total_size_mb']} MB")
    print(f"Unique Players: {summary['unique_players']}")
    print("\nBy Type:")
    
    for transfer_type, stats in summary['by_type'].items():
        if stats['count'] > 0:
            print(f"  {transfer_type}: {stats['count']} files ({stats['size_mb']} MB)")


def example_player_transfers():
    """Get transfers for specific player"""
    saved_arks = Path("C:/ASA_Servers/ShooterGame/Saved/SavedArks")
    steam_id = "76561198000000000"  # Replace with real Steam ID
    
    print(f"=== Transfers for Player {steam_id} ===\n")
    
    transfers = get_player_cluster_data(saved_arks, steam_id)
    
    if not transfers:
        print("No transfers found for this player")
        return
    
    print(f"Found {len(transfers)} transfers:\n")
    
    for t in transfers:
        print(f"{t.transfer_type}: {t.file_name}")
        if t.character_name:
            print(f"  Character: {t.character_name}")
        if t.upload_time:
            from datetime import datetime
            dt = datetime.fromtimestamp(t.upload_time)
            print(f"  Uploaded: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print()


def example_discord_command():
    """Example Discord bot command for cluster data"""
    import discord
    from discord import app_commands
    
    # This would be part of a Discord bot cog
    class ClusterCog:
        @app_commands.command(name="clusterstatus")
        async def cluster_status(self, interaction: discord.Interaction):
            """Show cluster transfer statistics"""
            
            saved_arks = Path("C:/ASA_Servers/ShooterGame/Saved/SavedArks")
            summary = get_cluster_summary(saved_arks)
            
            embed = discord.Embed(
                title="🌐 Cluster Status",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Total Transfers",
                value=f"{summary['total_files']} files",
                inline=True
            )
            
            embed.add_field(
                name="Storage Used",
                value=f"{summary['total_size_mb']} MB",
                inline=True
            )
            
            embed.add_field(
                name="Active Players",
                value=f"{summary['unique_players']} players",
                inline=True
            )
            
            # Breakdown by type
            breakdown = []
            for t_type, stats in summary['by_type'].items():
                if stats['count'] > 0:
                    breakdown.append(f"{t_type.title()}: {stats['count']}")
            
            if breakdown:
                embed.add_field(
                    name="By Type",
                    value="\n".join(breakdown),
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed)
    
    print("Discord command example shown above")


if __name__ == "__main__":
    print("=== ARK ASA Cluster Transfer Examples ===\n")
    
    examples = [
        ("Scan Cluster", example_scan_cluster),
        ("Cluster Summary", example_cluster_summary),
        ("Player Transfers", example_player_transfers),
        ("Discord Command", example_discord_command),
    ]
    
    for name, func in examples:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
