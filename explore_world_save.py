"""Explore world save database structure for dino data"""
import sqlite3
from pathlib import Path

world_path = Path(r"R:\PhoenixArk\asaserver_aberration\ShooterGame\Saved\SavedArks\Aberration_WP\Aberration_WP.ark")

if not world_path.exists():
    print("World save not found")
    exit(1)

conn = sqlite3.connect(str(world_path))
cursor = conn.cursor()

# Get table schema
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]

print(f"World Save: {world_path.name}")
print(f"Size: {world_path.stat().st_size / (1024**2):.1f} MB\n")
print(f"Tables: {', '.join(tables)}\n")

for table in tables:
    cursor.execute(f"PRAGMA table_info({table})")
    columns = cursor.fetchall()
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    
    print(f"Table: {table}")
    print(f"  Row count: {count:,}")
    print(f"  Columns: {', '.join(col[1] for col in columns)}")
    
    # Sample a row if exists
    if count > 0:
        cursor.execute(f"SELECT * FROM {table} LIMIT 1")
        sample = cursor.fetchone()
        if sample and len(columns) > 0:
            print(f"  Sample row (first column): {str(sample[0])[:100]}")
    print()

conn.close()