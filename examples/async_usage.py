"""
Example: Async usage for Discord bots and async applications
Requires: pip install ark-asa-parser[async]
"""
import asyncio
from pathlib import Path
from ark_asa_parser import AsyncArkSaveReader, async_scan_all_servers


async def example_async_players():
    """Read all players from a server asynchronously"""
    save_dir = Path("R:/PhoenixArk/asaserver_island/ShooterGame/Saved/SavedArks/TheIsland_WP")
    
    reader = AsyncArkSaveReader(save_dir)
    
    # Non-blocking file I/O - perfect for Discord bots
    players = await reader.async_get_all_players()
    
    print(f"Found {len(players)} players")
    for player in players[:5]:
        print(f"  {player.character_name or player.player_name} (Lvl {player.level})")


async def example_async_cluster():
    """Scan entire cluster asynchronously"""
    cluster_root = Path("R:/PhoenixArk")
    
    # Scan all servers
    readers = await async_scan_all_servers(cluster_root)
    
    print(f"Found {len(readers)} servers")
    
    # Process all servers concurrently
    tasks = []
    for server_name, reader in readers.items():
        tasks.append(process_server(server_name, reader))
    
    results = await asyncio.gather(*tasks)
    
    # Aggregate results
    total_players = sum(count for count, _ in results)
    total_tribes = sum(tribes for _, tribes in results)
    
    print(f"\nCluster totals: {total_players} players, {total_tribes} tribes")


async def process_server(name: str, reader: AsyncArkSaveReader):
    """Process a single server"""
    players = await reader.async_get_all_players()
    tribes = await reader.async_get_all_tribes()
    
    print(f"  {name}: {len(players)} players, {len(tribes)} tribes")
    
    return len(players), len(tribes)


async def example_discord_bot_command():
    """
    Example Discord.py command using async reader.
    No blocking on file I/O!
    """
    # This would be inside a Discord bot cog
    save_dir = Path("R:/PhoenixArk/asaserver_island/ShooterGame/Saved/SavedArks/TheIsland_WP")
    reader = AsyncArkSaveReader(save_dir)
    
    # In a real bot, you'd await interaction.response.defer() first
    players = await reader.async_get_all_players()
    
    # Build embed with player data
    player_list = "\n".join(
        f"{p.character_name} (Lvl {p.level})" 
        for p in sorted(players, key=lambda x: x.level, reverse=True)[:10]
    )
    
    print(f"Top 10 players:\n{player_list}")
    # In real bot: await interaction.followup.send(embed=embed)


if __name__ == "__main__":
    # Run examples
    print("=== Async Player Reading ===")
    asyncio.run(example_async_players())
    
    print("\n=== Async Cluster Scan ===")
    asyncio.run(example_async_cluster())
    
    print("\n=== Discord Bot Pattern ===")
    asyncio.run(example_discord_bot_command())