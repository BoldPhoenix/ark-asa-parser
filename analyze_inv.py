from pathlib import Path
import struct
from collections import Counter

# Check multiple servers
roots = [
    r'R:\PhoenixArk\asaserver_astraeos\ShooterGame\Saved\SavedArks\Astraeos_WP',
    r'R:\PhoenixArk\asaserver_amissa\ShooterGame\Saved\SavedArks\Amissa',
]

best_profile = None
best_item_count = 0

for root in roots:
    p = Path(root)
    if not p.exists():
        continue
    for profile in p.glob('*.arkprofile'):
        data = profile.read_bytes()
        item_count = data.count(b'ItemQuantity')
        if item_count > best_item_count:
            best_item_count = item_count
            best_profile = (profile, data)

if best_profile:
    profile, data = best_profile
    print(f'Profile: {profile.name}')
    print(f'Size: {len(data):,} bytes')
    print(f'ItemQuantity: {data.count(b"ItemQuantity")}')
    print(f'CustomItemName: {data.count(b"CustomItemName")}')
    print(f'ItemName: {data.count(b"ItemName")}')
    
    # Find property names before ArrayProperty
    pos = 0
    arrays_found = []
    while True:
        pos = data.find(b'ArrayProperty', pos)
        if pos == -1:
            break
        # Look back for property name (UE string: int32 len + chars + null)
        if pos > 50:
            try:
                for offset in range(4, 50):
                    check_pos = pos - offset
                    if check_pos >= 4:
                        length = struct.unpack('<i', data[check_pos-4:check_pos])[0]
                        if 3 < length < 40:
                            try:
                                name = data[check_pos:check_pos+length-1].decode('ascii')
                                if name.isascii() and name.isprintable():
                                    arrays_found.append(name)
                                    break
                            except:
                                pass
            except:
                pass
        pos += 1
    
    if arrays_found:
        counts = Counter(arrays_found)
        print(f'\nArrayProperty names:')
        for name, count in counts.most_common(10):
            print(f'  {name:30s}: {count}')
else:
    print('No profiles with items found')