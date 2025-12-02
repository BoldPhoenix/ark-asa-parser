"""
Example usage of full player stats extraction.

Shows how to get health, stamina, weight, and other detailed character attributes.
"""
from pathlib import Path
from ark_asa_parser import ArkSaveReader
from ark_asa_parser.player_stats import PlayerStatsReader


def example_basic_stats():
    """Get basic player stats from profiles"""
    save_dir = Path("SavedArks/TheIsland")
    
    if not save_dir.exists():
        print(f"Save directory not found: {save_dir}")
        return
    
    reader = ArkSaveReader(save_dir)
    players = reader.get_all_players()
    
    print("=== Player Stats ===\n")
    
    for player in players[:5]:  # First 5 players
        if not player.file_path:
            continue
        
        stats = PlayerStatsReader.read_player_stats(Path(player.file_path))
        
        print(f"{player.character_name or player.player_name}")
        print(f"  Level: {player.level}")
        
        if stats:
            for stat_name, value in sorted(stats.items()):
                print(f"  {stat_name}: {value:.1f}")
        else:
            print("  (No detailed stats found)")
        
        print()


def example_stat_summary():
    """Get formatted stat summary"""
    save_dir = Path("SavedArks/TheIsland")
    player_dir = save_dir / "Players"
    
    if not player_dir.exists():
        print(f"Player directory not found: {player_dir}")
        return
    
    print("=== Player Stat Summaries ===\n")
    
    for profile in list(player_dir.glob("*.arkprofile"))[:3]:
        summary = PlayerStatsReader.get_stat_summary(profile)
        
        print(f"{profile.name}")
        
        # Core stats
        if 'health' in summary:
            print(f"  💚 Health: {summary['health']:.0f}")
        if 'stamina' in summary:
            print(f"  💨 Stamina: {summary['stamina']:.0f}")
        if 'weight' in summary:
            print(f"  ⚖️  Weight: {summary['weight']:.0f}")
        
        # Other stats
        if 'oxygen' in summary:
            print(f"  🫁 Oxygen: {summary['oxygen']:.0f}")
        if 'food' in summary:
            print(f"  🍖 Food: {summary['food']:.0f}")
        if 'water' in summary:
            print(f"  💧 Water: {summary['water']:.0f}")
        
        # Combat/utility
        if 'melee' in summary:
            print(f"  ⚔️  Melee: {summary['melee']:.1f}%")
        if 'speed' in summary:
            print(f"  🏃 Speed: {summary['speed']:.1f}%")
        if 'fortitude' in summary:
            print(f"  🛡️  Fortitude: {summary['fortitude']:.0f}")
        
        print()


def example_discord_stats_embed():
    """Example Discord embed with player stats"""
    import discord
    from discord import app_commands
    
    class StatsCog:
        @app_commands.command(name="playerstats")
        @app_commands.describe(eos_id="Player EOS ID")
        async def player_stats(self, interaction: discord.Interaction, eos_id: str):
            """Show detailed player statistics"""
            
            save_dir = Path("SavedArks/TheIsland")
            reader = ArkSaveReader(save_dir)
            players = reader.get_all_players()
            
            # Find player
            player = next((p for p in players if p.eos_id == eos_id), None)
            if not player or not player.file_path:
                await interaction.response.send_message("❌ Player not found")
                return
            
            # Get stats
            stats = PlayerStatsReader.get_stat_summary(Path(player.file_path))
            
            if not stats:
                await interaction.response.send_message("❌ No stats available")
                return
            
            # Create embed
            embed = discord.Embed(
                title=f"📊 Stats for {player.character_name or player.player_name}",
                color=discord.Color.blue()
            )
            
            # Core stats
            core = []
            if 'health' in stats:
                core.append(f"💚 Health: **{stats['health']:.0f}**")
            if 'stamina' in stats:
                core.append(f"💨 Stamina: **{stats['stamina']:.0f}**")
            if 'weight' in stats:
                core.append(f"⚖️  Weight: **{stats['weight']:.0f}**")
            
            if core:
                embed.add_field(name="Core Stats", value="\n".join(core), inline=True)
            
            # Survival stats
            survival = []
            if 'oxygen' in stats:
                survival.append(f"🫁 Oxygen: {stats['oxygen']:.0f}")
            if 'food' in stats:
                survival.append(f"🍖 Food: {stats['food']:.0f}")
            if 'water' in stats:
                survival.append(f"💧 Water: {stats['water']:.0f}")
            
            if survival:
                embed.add_field(name="Survival", value="\n".join(survival), inline=True)
            
            # Combat
            combat = []
            if 'melee' in stats:
                combat.append(f"⚔️  Melee: {stats['melee']:.1f}%")
            if 'speed' in stats:
                combat.append(f"🏃 Speed: {stats['speed']:.1f}%")
            if 'fortitude' in stats:
                combat.append(f"🛡️  Fort: {stats['fortitude']:.0f}")
            
            if combat:
                embed.add_field(name="Combat", value="\n".join(combat), inline=True)
            
            embed.set_footer(text=f"Level {stats.get('level', '?')}")
            
            await interaction.response.send_message(embed=embed)
    
    print("Discord command example shown above")


def example_compare_players():
    """Compare stats between multiple players"""
    save_dir = Path("SavedArks/TheIsland")
    reader = ArkSaveReader(save_dir)
    players = reader.get_all_players()
    
    print("=== Player Stat Comparison ===\n")
    print(f"{'Player':<20} {'Health':>8} {'Stamina':>8} {'Weight':>8} {'Melee':>8}")
    print("-" * 60)
    
    for player in players[:10]:
        if not player.file_path:
            continue
        
        stats = PlayerStatsReader.get_stat_summary(Path(player.file_path))
        
        name = (player.character_name or player.player_name or "Unknown")[:19]
        health = f"{stats.get('health', 0):.0f}" if stats.get('health') else "-"
        stamina = f"{stats.get('stamina', 0):.0f}" if stats.get('stamina') else "-"
        weight = f"{stats.get('weight', 0):.0f}" if stats.get('weight') else "-"
        melee = f"{stats.get('melee', 0):.0f}%" if stats.get('melee') else "-"
        
        print(f"{name:<20} {health:>8} {stamina:>8} {weight:>8} {melee:>8}")


if __name__ == "__main__":
    print("=== ARK ASA Player Stats Examples ===\n")
    
    examples = [
        ("Basic Stats", example_basic_stats),
        ("Stat Summary", example_stat_summary),
        ("Player Comparison", example_compare_players),
        ("Discord Embed", example_discord_stats_embed),
    ]
    
    for name, func in examples:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
