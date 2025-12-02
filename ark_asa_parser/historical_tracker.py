"""
Historical data tracking and analytics.

Stores parsed ARK data in SQLite database for historical analysis,
trend tracking, and generating reports over time.
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict


@dataclass
class PlayerSnapshot:
    """Player state at a point in time"""
    timestamp: datetime
    eos_id: str
    player_name: str
    character_name: str
    level: int
    experience: float
    tribe_id: int
    server_name: str


@dataclass
class TribeSnapshot:
    """Tribe state at a point in time"""
    timestamp: datetime
    tribe_id: int
    tribe_name: str
    member_count: int
    server_name: str


class HistoricalTracker:
    """Track and analyze ARK data over time"""
    
    def __init__(self, db_path: Path):
        """
        Initialize historical tracker.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Player history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                eos_id TEXT NOT NULL,
                player_name TEXT,
                character_name TEXT,
                level INTEGER,
                experience REAL,
                tribe_id INTEGER,
                server_name TEXT,
                UNIQUE(timestamp, eos_id, server_name)
            )
        ''')
        
        # Tribe history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tribe_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                tribe_id INTEGER NOT NULL,
                tribe_name TEXT,
                member_count INTEGER,
                server_name TEXT,
                UNIQUE(timestamp, tribe_id, server_name)
            )
        ''')
        
        # Activity log table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                eos_id TEXT,
                server_name TEXT,
                details TEXT
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_history_eos ON player_history(eos_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_player_history_timestamp ON player_history(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_tribe_history_id ON tribe_history(tribe_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_activity_timestamp ON activity_log(timestamp)')
        
        conn.commit()
        conn.close()
    
    def record_player_snapshot(self, snapshot: PlayerSnapshot):
        """Record a player's state at current time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO player_history 
                (timestamp, eos_id, player_name, character_name, level, experience, tribe_id, server_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                snapshot.timestamp.isoformat(),
                snapshot.eos_id,
                snapshot.player_name,
                snapshot.character_name,
                snapshot.level,
                snapshot.experience,
                snapshot.tribe_id,
                snapshot.server_name
            ))
            conn.commit()
        finally:
            conn.close()
    
    def record_tribe_snapshot(self, snapshot: TribeSnapshot):
        """Record a tribe's state at current time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO tribe_history
                (timestamp, tribe_id, tribe_name, member_count, server_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                snapshot.timestamp.isoformat(),
                snapshot.tribe_id,
                snapshot.tribe_name,
                snapshot.member_count,
                snapshot.server_name
            ))
            conn.commit()
        finally:
            conn.close()
    
    def log_activity(self, event_type: str, eos_id: Optional[str] = None, 
                     server_name: Optional[str] = None, details: Optional[str] = None):
        """Log an activity event"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO activity_log (timestamp, event_type, eos_id, server_name, details)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                event_type,
                eos_id,
                server_name,
                details
            ))
            conn.commit()
        finally:
            conn.close()
    
    def get_player_history(self, eos_id: str, days: int = 30) -> List[Dict]:
        """Get player's historical data"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        try:
            cursor.execute('''
                SELECT timestamp, level, experience, server_name
                FROM player_history
                WHERE eos_id = ? AND timestamp >= ?
                ORDER BY timestamp ASC
            ''', (eos_id, cutoff.isoformat()))
            
            rows = cursor.fetchall()
            return [
                {
                    'timestamp': row[0],
                    'level': row[1],
                    'experience': row[2],
                    'server_name': row[3]
                }
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_player_level_progression(self, eos_id: str) -> List[Dict]:
        """Get player's level progression over time"""
        history = self.get_player_history(eos_id)
        
        progression = []
        last_level = 0
        
        for entry in history:
            if entry['level'] > last_level:
                progression.append({
                    'timestamp': entry['timestamp'],
                    'level': entry['level'],
                    'level_gain': entry['level'] - last_level
                })
                last_level = entry['level']
        
        return progression
    
    def get_tribe_growth(self, tribe_id: int, days: int = 30) -> List[Dict]:
        """Get tribe's member count over time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        try:
            cursor.execute('''
                SELECT timestamp, member_count, server_name
                FROM tribe_history
                WHERE tribe_id = ? AND timestamp >= ?
                ORDER BY timestamp ASC
            ''', (tribe_id, cutoff.isoformat()))
            
            rows = cursor.fetchall()
            return [
                {
                    'timestamp': row[0],
                    'member_count': row[1],
                    'server_name': row[2]
                }
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_active_players(self, hours: int = 24) -> List[str]:
        """Get list of players active in the last N hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(hours=hours)
        
        try:
            cursor.execute('''
                SELECT DISTINCT eos_id
                FROM player_history
                WHERE timestamp >= ?
            ''', (cutoff.isoformat(),))
            
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()
    
    def get_server_population_history(self, server_name: str, days: int = 7) -> List[Dict]:
        """Get server population over time"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        try:
            cursor.execute('''
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(DISTINCT eos_id) as unique_players
                FROM player_history
                WHERE server_name = ? AND timestamp >= ?
                GROUP BY DATE(timestamp)
                ORDER BY date ASC
            ''', (server_name, cutoff.isoformat()))
            
            rows = cursor.fetchall()
            return [
                {
                    'date': row[0],
                    'unique_players': row[1]
                }
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_top_level_gainers(self, days: int = 7, limit: int = 10) -> List[Dict]:
        """Get players who gained the most levels recently"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        try:
            cursor.execute('''
                SELECT 
                    eos_id,
                    player_name,
                    MAX(level) - MIN(level) as level_gain,
                    MIN(level) as start_level,
                    MAX(level) as end_level
                FROM player_history
                WHERE timestamp >= ?
                GROUP BY eos_id
                HAVING level_gain > 0
                ORDER BY level_gain DESC
                LIMIT ?
            ''', (cutoff.isoformat(), limit))
            
            rows = cursor.fetchall()
            return [
                {
                    'eos_id': row[0],
                    'player_name': row[1],
                    'level_gain': row[2],
                    'start_level': row[3],
                    'end_level': row[4]
                }
                for row in rows
            ]
        finally:
            conn.close()
    
    def get_activity_summary(self, days: int = 7) -> Dict:
        """Get summary of recent activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        try:
            # Count events by type
            cursor.execute('''
                SELECT event_type, COUNT(*) as count
                FROM activity_log
                WHERE timestamp >= ?
                GROUP BY event_type
            ''', (cutoff.isoformat(),))
            
            events = {row[0]: row[1] for row in cursor.fetchall()}
            
            # Unique players
            cursor.execute('''
                SELECT COUNT(DISTINCT eos_id)
                FROM player_history
                WHERE timestamp >= ?
            ''', (cutoff.isoformat(),))
            
            unique_players = cursor.fetchone()[0]
            
            return {
                'period_days': days,
                'unique_players': unique_players,
                'events': events
            }
        finally:
            conn.close()
    
    def cleanup_old_data(self, days: int = 90):
        """Remove data older than specified days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(days=days)
        
        try:
            cursor.execute('DELETE FROM player_history WHERE timestamp < ?', (cutoff.isoformat(),))
            cursor.execute('DELETE FROM tribe_history WHERE timestamp < ?', (cutoff.isoformat(),))
            cursor.execute('DELETE FROM activity_log WHERE timestamp < ?', (cutoff.isoformat(),))
            
            deleted = cursor.rowcount
            conn.commit()
            
            # Vacuum to reclaim space
            cursor.execute('VACUUM')
            
            return deleted
        finally:
            conn.close()