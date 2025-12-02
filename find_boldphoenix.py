"""Find BoldPhoenix's XP value"""
from pathlib import Path
from ark_asa_parser import simple_property_reader
from ark_asa_parser.levels import xp_to_level
from ark_asa_parser.xp_data import get_default_xp_table

table = get_default_xp_table()
profiles = list(Path('R:/PhoenixArk').rglob('*.arkprofile'))

print('Searching for BoldPhoenix...\n')
for pf in profiles:
    with open(pf, 'rb') as f:
        data = f.read()
    
    char_name = simple_property_reader.find_string_property(data, 'PlayerCharacterName') or ''
    
    if 'boldphoenix' in char_name.lower():
        exp = simple_property_reader.find_float_property(data, 'CharacterStatusComponent_ExperiencePoints') or 0
        level = xp_to_level(exp, xp_table=table) if exp > 0 else 1
        print(f'Found: {char_name}')
        print(f'  XP: {exp}')
        print(f'  Calculated Level: {level}')
        print(f'  (User says actual level is 135)')
        print()
        
        # Check what XP level 135 should require
        if len(table) >= 135:
            print(f'  Level 135 requires: {table[134]} XP')
            print(f'  Level 136 requires: {table[135]} XP')
