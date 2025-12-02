"""Search for ALL property names in an ARK profile"""
from pathlib import Path
import re

profile_dir = Path("R:/PhoenixArk")
profile_files = list(profile_dir.rglob("*.arkprofile"))

if profile_files:
    pf = profile_files[0]  # First file
    print(f"Examining: {pf.name}\n")
    
    with open(pf, 'rb') as f:
        data = f.read()
    
    # Find all null-terminated strings that look like property names
    # Property names in UE are often preceded by their length as int32
    properties = set()
    
    i = 0
    while i < len(data) - 20:
        # Check if this looks like a length-prefixed string
        try:
            # Try reading as little-endian int32 for string length
            str_len = int.from_bytes(data[i:i+4], 'little', signed=True)
            
            # Reasonable string length (1-200 chars)
            if 1 < str_len < 200:
                try:
                    # Try to decode the string
                    string = data[i+4:i+4+str_len-1].decode('ascii')
                    # Check if it looks like a property name (alphanumeric with some special chars)
                    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', string) and len(string) > 3:
                        properties.add(string)
                except:
                    pass
        except:
            pass
        
        i += 1
    
    print(f"Found {len(properties)} potential property names:\n")
    
    # Filter for interesting ones
    interesting = sorted([p for p in properties if any(keyword in p.lower() for keyword in 
                         ['exp', 'level', 'xp', 'character', 'stat', 'point'])])
    
    print("Properties containing 'exp', 'level', 'xp', 'character', 'stat', or 'point':")
    for prop in interesting:
        print(f"  {prop}")
else:
    print("No profile files found!")
