"""
Real-time save file watching and change detection.

Monitors ARK save directories for file changes and emits events
for player joins/leaves, dino tames, deaths, and other game events.
"""
import time
from pathlib import Path
from typing import Callable, Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import asyncio
from threading import Thread


@dataclass
class SaveFileEvent:
    """Represents a save file change event"""
    event_type: str  # 'player_join', 'player_leave', 'file_modified', 'file_created', 'file_deleted'
    file_path: Path
    timestamp: datetime
    player_id: Optional[str] = None
    player_name: Optional[str] = None
    details: Optional[Dict] = None


class SaveWatcher:
    """Watch save directory for changes and emit events"""
    
    def __init__(self, save_dir: Path, poll_interval: float = 5.0):
        """
        Initialize save watcher.
        
        Args:
            save_dir: Path to ARK save directory to watch
            poll_interval: Seconds between directory scans
        """
        self.save_dir = Path(save_dir)
        self.poll_interval = poll_interval
        self.running = False
        self._thread: Optional[Thread] = None
        self._callbacks: List[Callable[[SaveFileEvent], None]] = []
        self._file_states: Dict[Path, dict] = {}
        self._known_players: Set[str] = set()
    
    def add_callback(self, callback: Callable[[SaveFileEvent], None]):
        """Add a callback function to be called on events"""
        self._callbacks.append(callback)
    
    def remove_callback(self, callback: Callable[[SaveFileEvent], None]):
        """Remove a callback function"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def _emit_event(self, event: SaveFileEvent):
        """Call all registered callbacks with the event"""
        for callback in self._callbacks:
            try:
                callback(event)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    def _scan_directory(self):
        """Scan save directory and detect changes"""
        if not self.save_dir.exists():
            return
        
        current_files = {}
        
        # Scan all relevant files
        for pattern in ['*.arkprofile', '*.arktribe', '*.ark']:
            for file_path in self.save_dir.rglob(pattern):
                try:
                    stat = file_path.stat()
                    current_files[file_path] = {
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'exists': True
                    }
                except:
                    continue
        
        # Detect changes
        for file_path, current_state in current_files.items():
            if file_path not in self._file_states:
                # New file
                event = SaveFileEvent(
                    event_type='file_created',
                    file_path=file_path,
                    timestamp=datetime.now()
                )
                
                # Check if it's a player profile
                if file_path.suffix == '.arkprofile':
                    player_id = file_path.stem
                    if player_id not in self._known_players:
                        self._known_players.add(player_id)
                        event.event_type = 'player_join'
                        event.player_id = player_id
                
                self._emit_event(event)
            
            elif current_state['mtime'] != self._file_states[file_path]['mtime']:
                # File modified
                event = SaveFileEvent(
                    event_type='file_modified',
                    file_path=file_path,
                    timestamp=datetime.now(),
                    details={
                        'old_size': self._file_states[file_path]['size'],
                        'new_size': current_state['size']
                    }
                )
                self._emit_event(event)
        
        # Detect deletions
        for file_path in list(self._file_states.keys()):
            if file_path not in current_files:
                event = SaveFileEvent(
                    event_type='file_deleted',
                    file_path=file_path,
                    timestamp=datetime.now()
                )
                self._emit_event(event)
                del self._file_states[file_path]
        
        # Update states
        self._file_states = current_files
    
    def _watch_loop(self):
        """Main watch loop (runs in thread)"""
        while self.running:
            try:
                self._scan_directory()
                time.sleep(self.poll_interval)
            except Exception as e:
                print(f"Error in watch loop: {e}")
                time.sleep(self.poll_interval)
    
    def start(self):
        """Start watching the save directory"""
        if self.running:
            return
        
        self.running = True
        self._thread = Thread(target=self._watch_loop, daemon=True)
        self._thread.start()
    
    def stop(self):
        """Stop watching the save directory"""
        self.running = False
        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None
    
    def __enter__(self):
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()


class AsyncSaveWatcher:
    """Async version of SaveWatcher for use with asyncio"""
    
    def __init__(self, save_dir: Path, poll_interval: float = 5.0):
        self.save_dir = Path(save_dir)
        self.poll_interval = poll_interval
        self.running = False
        self._task: Optional[asyncio.Task] = None
        self._callbacks: List[Callable[[SaveFileEvent], None]] = []
        self._file_states: Dict[Path, dict] = {}
        self._known_players: Set[str] = set()
    
    def add_callback(self, callback: Callable[[SaveFileEvent], None]):
        """Add a callback function to be called on events"""
        self._callbacks.append(callback)
    
    def remove_callback(self, callback: Callable[[SaveFileEvent], None]):
        """Remove a callback function"""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    async def _emit_event(self, event: SaveFileEvent):
        """Call all registered callbacks with the event"""
        for callback in self._callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(event)
                else:
                    callback(event)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    async def _scan_directory(self):
        """Scan save directory and detect changes"""
        if not self.save_dir.exists():
            return
        
        current_files = {}
        
        # Scan all relevant files
        for pattern in ['*.arkprofile', '*.arktribe', '*.ark']:
            for file_path in self.save_dir.rglob(pattern):
                try:
                    stat = file_path.stat()
                    current_files[file_path] = {
                        'size': stat.st_size,
                        'mtime': stat.st_mtime,
                        'exists': True
                    }
                except:
                    continue
        
        # Detect changes
        for file_path, current_state in current_files.items():
            if file_path not in self._file_states:
                # New file
                event = SaveFileEvent(
                    event_type='file_created',
                    file_path=file_path,
                    timestamp=datetime.now()
                )
                
                # Check if it's a player profile
                if file_path.suffix == '.arkprofile':
                    player_id = file_path.stem
                    if player_id not in self._known_players:
                        self._known_players.add(player_id)
                        event.event_type = 'player_join'
                        event.player_id = player_id
                
                await self._emit_event(event)
            
            elif current_state['mtime'] != self._file_states[file_path]['mtime']:
                # File modified
                event = SaveFileEvent(
                    event_type='file_modified',
                    file_path=file_path,
                    timestamp=datetime.now(),
                    details={
                        'old_size': self._file_states[file_path]['size'],
                        'new_size': current_state['size']
                    }
                )
                await self._emit_event(event)
        
        # Detect deletions
        for file_path in list(self._file_states.keys()):
            if file_path not in current_files:
                event = SaveFileEvent(
                    event_type='file_deleted',
                    file_path=file_path,
                    timestamp=datetime.now()
                )
                await self._emit_event(event)
                del self._file_states[file_path]
        
        # Update states
        self._file_states = current_files
    
    async def _watch_loop(self):
        """Main async watch loop"""
        while self.running:
            try:
                await self._scan_directory()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                print(f"Error in watch loop: {e}")
                await asyncio.sleep(self.poll_interval)
    
    async def start(self):
        """Start watching the save directory"""
        if self.running:
            return
        
        self.running = True
        self._task = asyncio.create_task(self._watch_loop())
    
    async def stop(self):
        """Stop watching the save directory"""
        self.running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
    
    async def __aenter__(self):
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()