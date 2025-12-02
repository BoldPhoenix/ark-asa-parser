"""
Performance testing examples for ark-asa-parser.

Shows how to profile, benchmark, and optimize save file parsing.
"""
from pathlib import Path
from ark_asa_parser import ArkSaveReader
from ark_asa_parser.performance import (
    profile_function,
    benchmark_file_read,
    OptimizedReader,
    get_optimization_recommendations,
    mmap_file
)


def example_profile_reader():
    """Profile player reading to find bottlenecks"""
    save_path = Path("SavedArks/TheIsland")
    reader = ArkSaveReader(save_path)
    
    # Profile the get_all_players call
    players, stats = profile_function(reader.get_all_players)
    
    print(f"Found {len(players)} players")
    print("\nTop 10 time-consuming operations:")
    stats.sort_stats('cumulative').print_stats(10)
    
    print("\nFunctions called most frequently:")
    stats.sort_stats('ncalls').print_stats(10)


def example_benchmark_file_methods():
    """Compare different file reading approaches"""
    profile_path = Path("SavedArks/TheIsland/Players/00000000000000000.arkprofile")
    
    if not profile_path.exists():
        print(f"Profile not found: {profile_path}")
        return
    
    print(f"Benchmarking {profile_path.name}...")
    
    methods = ['read', 'mmap', 'chunks']
    for method in methods:
        time = benchmark_file_read(profile_path, method)
        print(f"{method:>8}: {time*1000:.2f}ms")


def example_optimization_recommendations():
    """Get optimization recommendations for files"""
    save_path = Path("SavedArks/TheIsland")
    
    print("Optimization Recommendations:\n")
    
    # Check player profiles
    player_dir = save_path / "Players"
    if player_dir.exists():
        for profile in list(player_dir.glob("*.arkprofile"))[:3]:
            rec = get_optimization_recommendations(profile)
            print(f"{profile.name}:")
            print(f"  Size: {rec['file_size_mb']:.2f} MB")
            print(f"  Use mmap: {rec['use_mmap']}")
            print(f"  Use async: {rec['use_async']}")
            print(f"  Note: {rec['note']}")
            print()


def example_mmap_search():
    """Use memory-mapped file for efficient searching"""
    profile_path = Path("SavedArks/TheIsland/Players/00000000000000000.arkprofile")
    
    if not profile_path.exists():
        print(f"Profile not found: {profile_path}")
        return
    
    # Memory-map the file
    with mmap_file(profile_path) as mm:
        # Search for properties
        player_name_pos = mm.find(b"PlayerName")
        level_pos = mm.find(b"CharacterLevel")
        
        print(f"PlayerName at offset: {player_name_pos}")
        print(f"CharacterLevel at offset: {level_pos}")
        
        # Count occurrences
        inventory_count = mm.read().count(b"InventoryItems")
        print(f"InventoryItems references: {inventory_count}")


def example_optimized_reader():
    """Use OptimizedReader for large files"""
    profile_path = Path("SavedArks/TheIsland/Players/00000000000000000.arkprofile")
    
    if not profile_path.exists():
        print(f"Profile not found: {profile_path}")
        return
    
    with OptimizedReader(profile_path) as reader:
        print(f"File size: {reader.size / 1024:.2f} KB")
        
        # Find all PlayerName occurrences
        positions = reader.find_all(b"PlayerName", limit=5)
        print(f"Found PlayerName at positions: {positions}")
        
        # Read chunk around first occurrence
        if positions:
            chunk = reader.read_chunk(positions[0] - 20, 100)
            print(f"Context: {chunk[:50]}...")


def example_compare_sync_async():
    """Compare sync vs async performance for multiple files"""
    import time
    import asyncio
    from ark_asa_parser import AsyncArkSaveReader
    
    save_path = Path("SavedArks/TheIsland")
    
    # Sync approach
    print("Testing sync reader...")
    start = time.perf_counter()
    sync_reader = ArkSaveReader(save_path)
    players = sync_reader.get_all_players()
    sync_time = time.perf_counter() - start
    print(f"Sync: {len(players)} players in {sync_time:.3f}s")
    
    # Async approach
    print("\nTesting async reader...")
    async def test_async():
        start = time.perf_counter()
        async_reader = AsyncArkSaveReader(save_path)
        players = await async_reader.async_get_all_players()
        return len(players), time.perf_counter() - start
    
    count, async_time = asyncio.run(test_async())
    print(f"Async: {count} players in {async_time:.3f}s")
    
    # Comparison
    speedup = sync_time / async_time if async_time > 0 else 0
    print(f"\nSpeedup: {speedup:.2f}x")


if __name__ == "__main__":
    print("=== ARK ASA Parser Performance Testing ===\n")
    
    # Run examples
    examples = [
        ("File Reading Benchmark", example_benchmark_file_methods),
        ("Optimization Recommendations", example_optimization_recommendations),
        ("Memory-Mapped Search", example_mmap_search),
        ("Optimized Reader", example_optimized_reader),
        ("Sync vs Async Comparison", example_compare_sync_async),
        # Profiling takes longer, uncomment to run:
        # ("Profile Reader", example_profile_reader),
    ]
    
    for name, func in examples:
        print(f"\n{'='*60}")
        print(f"{name}")
        print('='*60)
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
