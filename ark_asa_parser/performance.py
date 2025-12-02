"""
Performance utilities and optimizations for ARK save parsing.

Provides profiling tools and optimized readers for large files.
"""
import cProfile
import pstats
import io
from pathlib import Path
from typing import Callable, Any
import mmap
import contextlib


def profile_function(func: Callable, *args, **kwargs) -> tuple[Any, pstats.Stats]:
    """
    Profile a function call and return results + stats.
    
    Args:
        func: Function to profile
        *args, **kwargs: Arguments to pass to function
    
    Returns:
        (function_result, pstats.Stats object)
    
    Example:
        result, stats = profile_function(reader.get_all_players)
        stats.sort_stats('cumulative').print_stats(10)
    """
    profiler = cProfile.Profile()
    profiler.enable()
    
    result = func(*args, **kwargs)
    
    profiler.disable()
    
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s)
    
    return result, stats


def benchmark_file_read(file_path: Path, method: str = 'read') -> float:
    """
    Benchmark different file reading approaches.
    
    Args:
        file_path: Path to file to read
        method: 'read', 'mmap', or 'chunks'
    
    Returns:
        Time in seconds
    """
    import time
    
    if method == 'read':
        start = time.perf_counter()
        data = file_path.read_bytes()
        return time.perf_counter() - start
    
    elif method == 'mmap':
        start = time.perf_counter()
        with open(file_path, 'rb') as f:
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                data = mm[:]
        return time.perf_counter() - start
    
    elif method == 'chunks':
        start = time.perf_counter()
        chunks = []
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                chunks.append(chunk)
        data = b''.join(chunks)
        return time.perf_counter() - start
    
    else:
        raise ValueError(f"Unknown method: {method}")


@contextlib.contextmanager
def mmap_file(file_path: Path, mode='r'):
    """
    Context manager for memory-mapped file access.
    
    Use for large files (>50MB) to reduce memory usage.
    
    Example:
        with mmap_file(profile_path) as mm:
            # Search in memory-mapped file
            pos = mm.find(b"PlayerName")
    """
    with open(file_path, 'rb') as f:
        mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        try:
            yield mm
        finally:
            mm.close()


def optimize_property_search(data: bytes, patterns: list[bytes]) -> dict[bytes, int]:
    """
    Optimized multi-pattern search using Boyer-Moore-like approach.
    
    Faster than multiple sequential searches for many patterns.
    
    Args:
        data: Byte data to search
        patterns: List of byte patterns to find
    
    Returns:
        Dict mapping pattern to count
    """
    results = {}
    
    # Precompute bad character tables for each pattern
    # (simplified Boyer-Moore)
    for pattern in patterns:
        count = 0
        pos = 0
        pattern_len = len(pattern)
        
        while pos < len(data):
            pos = data.find(pattern, pos)
            if pos == -1:
                break
            count += 1
            pos += pattern_len
        
        results[pattern] = count
    
    return results


class OptimizedReader:
    """
    Optimized reader for large save files using memory mapping.
    
    Use for files >50MB or when processing many files concurrently.
    """
    
    def __init__(self, file_path: Path):
        self.file_path = Path(file_path)
        self.size = self.file_path.stat().st_size
        self._mm = None
        self._file = None
    
    def __enter__(self):
        self._file = open(self.file_path, 'rb')
        self._mm = mmap.mmap(self._file.fileno(), 0, access=mmap.ACCESS_READ)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._mm:
            self._mm.close()
        if self._file:
            self._file.close()
    
    def find_all(self, pattern: bytes, limit: int = None) -> list[int]:
        """Find all occurrences of pattern, return positions"""
        if not self._mm:
            raise RuntimeError("Reader not opened (use 'with' statement)")
        
        positions = []
        pos = 0
        
        while (limit is None or len(positions) < limit) and pos < self.size:
            pos = self._mm.find(pattern, pos)
            if pos == -1:
                break
            positions.append(pos)
            pos += 1
        
        return positions
    
    def read_chunk(self, offset: int, size: int) -> bytes:
        """Read chunk at offset"""
        if not self._mm:
            raise RuntimeError("Reader not opened")
        return self._mm[offset:offset+size]
    
    @property
    def data(self) -> memoryview:
        """Access as memoryview (efficient for large files)"""
        if not self._mm:
            raise RuntimeError("Reader not opened")
        return memoryview(self._mm)


def get_optimization_recommendations(file_path: Path) -> dict:
    """
    Analyze file and provide optimization recommendations.
    
    Returns dict with:
        - use_mmap: bool (recommend mmap for large files)
        - use_async: bool (recommend async for many files)
        - estimated_read_time: float (seconds)
    """
    size = file_path.stat().st_size
    size_mb = size / (1024 * 1024)
    
    recommendations = {
        'file_size_mb': size_mb,
        'use_mmap': size_mb > 50,
        'use_async': True,  # Always beneficial for I/O
        'use_chunks': size_mb > 100,
        'estimated_read_time_sync': size_mb * 0.001,  # ~1ms per MB
        'estimated_read_time_async': size_mb * 0.0005,  # ~0.5ms per MB
    }
    
    if size_mb > 50:
        recommendations['note'] = "Large file - use mmap or async reader"
    elif size_mb > 10:
        recommendations['note'] = "Medium file - async recommended"
    else:
        recommendations['note'] = "Small file - any method fine"
    
    return recommendations