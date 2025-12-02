"""
Comprehensive examples for dino extraction, structure extraction, 
save watching, and historical tracking.
"""
from pathlib import Path
from ark_asa_parser.dino_extractor import DinoExtractor
from ark_asa_parser.structure_extractor import StructureExtractor
from ark_asa_parser.save_watcher import SaveWatcher, AsyncSaveWatcher, SaveFileEvent
from ark_asa_parser.historical_tracker import HistoricalTracker, PlayerSnapshot, TribeSnapshot
from ark_asa_parser import ArkSaveReader
from datetime import datetime
import asyncio


def example_dino_extraction():
    """Extract tamed dinos from world save"""
    world_ark = Path("SavedArks/TheIsland/TheIsland_WP.ark")
    
    if not world_ark.exists():
        print(f"World save not found: {world_ark}")
        return
    
    print("=== Extracting Tamed Dinos ===\n")
    
    dinos = DinoExtractor.extract_dinos_from_world(world_ark)
    
    print(f"Found {len(dinos)} tamed dinos\n")
    
    for dino in dinos[:10]:  # First 10
        print(f"{dino.species_name}")
        if dino.dino_name:
            print(f"  Name: {dino.dino_name}")
        if dino.owner_name:
            print(f"  Owner: {dino.owner_name}")
        print(f"  Level: {dino.level}")
        if dino.tribe_id:
            print(f"  Tribe ID: {dino.tribe_id}")
        print()


def example_dino_summary():
    """Get dino species summary"""
    world_ark = Path("SavedArks/TheIsland/TheIsland_WP.ark")
    
    if not world_ark.exists():
        print(f"World save not found: {world_ark}")
        return
    
    print("=== Dino Species Summary ===\n")
    
    summary = DinoExtractor.get_dino_summary(world_ark)
    
    for species, count in list(summary.items())[:15]:
        print(f"{species:<30} {count:>4}")


def example_tribe_dinos():
    """Get all dinos for a specific tribe"""
    world_ark = Path("SavedArks/TheIsland/TheIsland_WP.ark")
    tribe_id = 1234567890  # Replace with actual tribe ID
    
    if not world_ark.exists():
        print(f"World save not found: {world_ark}")
        return
    
    print(f"=== Dinos for Tribe {tribe_id} ===\n")
    
    dinos = DinoExtractor.get_tribe_dinos(world_ark, tribe_id)
    
    print(f"Found {len(dinos)} dinos for this tribe\n")
    
    for dino in dinos:
        name = dino.dino_name or dino.species_name
        print(f"  - {name} (Level {dino.level})")


def example_structure_extraction():
    """Extract structures from world save"""
    world_ark = Path("SavedArks/TheIsland/TheIsland_WP.ark")
    
    if not world_ark.exists():
        print(f"World save not found: {world_ark}")
        return
    
    print("=== Extracting Structures ===\n")
    
    structures = StructureExtractor.extract_structures_from_world(world_ark)
    
    print(f"Found {len(structures)} structures\n")
    
    for structure in structures[:10]:  # First 10
        print(f"{structure.structure_type}")
        if structure.owner_name:
            print(f"  Owner: {structure.owner_name}")
        if structure.tribe_name:
            print(f"  Tribe: {structure.tribe_name}")
        if structure.is_locked:
            print(f"  🔒 Locked")
        print()


def example_structure_summary():
    """Get structure category summary"""
    world_ark = Path("SavedArks/TheIsland/TheIsland_WP.ark")
    
    if not world_ark.exists():
        print(f"World save not found: {world_ark}")
        return
    
    print("=== Structure Summary ===\n")
    
    summary = StructureExtractor.get_structure_summary(world_ark)
    
    print(f"Total Structures: {summary['total']}\n")
    
    print("By Category:")
    for category, count in summary['by_category'].items():
        print(f"  {category:<20} {count:>4}")
    
    print("\nTop Structure Types:")
    for struct_type, count in list(summary['by_type'].items())[:10]:
        print(f"  {struct_type:<30} {count:>4}")


def example_save_watching():
    """Watch save directory for changes"""
    save_dir = Path("SavedArks/TheIsland")
    
    if not save_dir.exists():
        print(f"Save directory not found: {save_dir}")
        return
    
    print("=== Watching Save Directory ===\n")
    print(f"Monitoring: {save_dir}")
    print("Press Ctrl+C to stop...\n")
    
    def on_event(event: SaveFileEvent):
        print(f"[{event.timestamp:%H:%M:%S}] {event.event_type}")
        print(f"  File: {event.file_path.name}")
        if event.player_id:
            print(f"  Player: {event.player_id}")
        if event.details:
            print(f"  Details: {event.details}")
        print()
    
    watcher = SaveWatcher(save_dir, poll_interval=10.0)
    watcher.add_callback(on_event)
    
    try:
        watcher.start()
        # Keep running
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        watcher.stop()


async def example_async_save_watching():
    """Async save watching for Discord bots"""
    save_dir = Path("SavedArks/TheIsland")
    
    if not save_dir.exists():
        print(f"Save directory not found: {save_dir}")
        return
    
    print("=== Async Save Watching ===\n")
    
    async def on_event(event: SaveFileEvent):
        if event.event_type == 'player_join':
            print(f"🎮 Player joined: {event.player_id}")
        elif event.event_type == 'file_modified':
            print(f"📝 File updated: {event.file_path.name}")
    
    watcher = AsyncSaveWatcher(save_dir, poll_interval=10.0)
    watcher.add_callback(on_event)
    
    await watcher.start()
    
    # Run for 60 seconds
    await asyncio.sleep(60)
    
    await watcher.stop()


def example_historical_tracking():
    """Track player data over time"""
    db_path = Path("ark_history.db")
    tracker = HistoricalTracker(db_path)
    
    print("=== Historical Tracking ===\n")
    
    # Record some player snapshots
    save_dir = Path("SavedArks/TheIsland")
    if save_dir.exists():
        reader = ArkSaveReader(save_dir)
        players = reader.get_all_players()
        
        for player in players[:5]:
            snapshot = PlayerSnapshot(
                timestamp=datetime.now(),
                eos_id=player.eos_id,
                player_name=player.player_name,
                character_name=player.character_name,
                level=player.level,
                experience=player.experience,
                tribe_id=player.tribe_id,
                server_name="TheIsland"
            )
            tracker.record_player_snapshot(snapshot)
        
        print(f"Recorded snapshots for {len(players[:5])} players")
    
    # Get activity summary
    summary = tracker.get_activity_summary(days=7)
    print(f"\nActivity Summary (Last 7 days):")
    print(f"  Unique Players: {summary['unique_players']}")
    print(f"  Events: {summary['events']}")


def example_player_progression():
    """Track player level progression"""
    db_path = Path("ark_history.db")
    tracker = HistoricalTracker(db_path)
    eos_id = "00000000000000000"  # Replace with actual EOS ID
    
    print(f"=== Player Progression for {eos_id} ===\n")
    
    progression = tracker.get_player_level_progression(eos_id)
    
    if not progression:
        print("No progression data found")
        return
    
    for entry in progression:
        print(f"{entry['timestamp']} - Level {entry['level']} (+{entry['level_gain']})")


def example_top_level_gainers():
    """Show top players by level gains"""
    db_path = Path("ark_history.db")
    tracker = HistoricalTracker(db_path)
    
    print("=== Top Level Gainers (Last 7 Days) ===\n")
    
    top_players = tracker.get_top_level_gainers(days=7, limit=10)
    
    for i, player in enumerate(top_players, 1):
        print(f"{i}. {player['player_name']}")
        print(f"   {player['start_level']} → {player['end_level']} (+{player['level_gain']})")


def example_discord_integration():
    """Example Discord bot integration"""
    import discord
    from discord import app_commands
    
    class AdvancedStatsCog:
        def __init__(self, bot):
            self.bot = bot
            self.tracker = HistoricalTracker(Path("ark_history.db"))
        
        @app_commands.command(name="dinos")
        @app_commands.describe(server="Server name")
        async def dino_list(self, interaction: discord.Interaction, server: str):
            """Show tamed dinos on server"""
            world_ark = Path(f"SavedArks/{server}/{server}_WP.ark")
            
            if not world_ark.exists():
                await interaction.response.send_message("❌ Server not found")
                return
            
            await interaction.response.defer()
            
            summary = DinoExtractor.get_dino_summary(world_ark)
            
            embed = discord.Embed(
                title=f"🦖 Tamed Dinos on {server.upper()}",
                color=discord.Color.green()
            )
            
            # Top species
            top_species = list(summary.items())[:10]
            species_text = "\n".join([f"{species}: **{count}**" for species, count in top_species])
            
            embed.add_field(name="Top Species", value=species_text or "None", inline=False)
            embed.set_footer(text=f"Total: {sum(summary.values())} dinos")
            
            await interaction.followup.send(embed=embed)
        
        @app_commands.command(name="structures")
        @app_commands.describe(server="Server name")
        async def structure_list(self, interaction: discord.Interaction, server: str):
            """Show structure summary"""
            world_ark = Path(f"SavedArks/{server}/{server}_WP.ark")
            
            if not world_ark.exists():
                await interaction.response.send_message("❌ Server not found")
                return
            
            await interaction.response.defer()
            
            summary = StructureExtractor.get_structure_summary(world_ark)
            
            embed = discord.Embed(
                title=f"🏗️ Structures on {server.upper()}",
                color=discord.Color.blue()
            )
            
            # By category
            category_text = "\n".join([
                f"{cat}: **{count}**" 
                for cat, count in summary['by_category'].items()
            ])
            
            embed.add_field(name="By Category", value=category_text or "None", inline=False)
            embed.set_footer(text=f"Total: {summary['total']} structures")
            
            await interaction.followup.send(embed=embed)
        
        @app_commands.command(name="progression")
        @app_commands.describe(eos_id="Player EOS ID")
        async def player_progression(self, interaction: discord.Interaction, eos_id: str):
            """Show player's level progression"""
            progression = self.tracker.get_player_level_progression(eos_id)
            
            if not progression:
                await interaction.response.send_message("❌ No progression data found")
                return
            
            embed = discord.Embed(
                title=f"📈 Level Progression",
                description=f"Player: {eos_id[:16]}...",
                color=discord.Color.gold()
            )
            
            # Recent levels
            recent = progression[-5:]
            progress_text = "\n".join([
                f"Level {entry['level']} (+{entry['level_gain']})"
                for entry in recent
            ])
            
            embed.add_field(name="Recent Levels", value=progress_text, inline=False)
            
            await interaction.response.send_message(embed=embed)
    
    print("Discord cog example shown above")


if __name__ == "__main__":
    print("=== ARK ASA Advanced Features Examples ===\n")
    
    examples = [
        ("Dino Extraction", example_dino_extraction),
        ("Dino Summary", example_dino_summary),
        ("Structure Extraction", example_structure_extraction),
        ("Structure Summary", example_structure_summary),
        ("Historical Tracking", example_historical_tracking),
        ("Top Level Gainers", example_top_level_gainers),
        ("Discord Integration", example_discord_integration),
        # Uncomment to test:
        # ("Save Watching", example_save_watching),
        # ("Async Save Watching", lambda: asyncio.run(example_async_save_watching())),
    ]
    
    for name, func in examples:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
