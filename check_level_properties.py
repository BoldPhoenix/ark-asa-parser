"""Check for level properties in profiles"""
from pathlib import Path
from ark_asa_parser import simple_property_reader

profiles = list(Path('R:/PhoenixArk').rglob('*.arkprofile'))[:10]

print('Checking for level-related properties:\n')
for pf in profiles:
    with open(pf, 'rb') as f:
        data = f.read()
    
    char_name = simple_property_reader.find_string_property(data, 'PlayerCharacterName') or 'Unknown'
    
    # Check various level properties
    char_level = simple_property_reader.find_int_property(data, 'CharacterLevel')
    player_level = simple_property_reader.find_int_property(data, 'PlayerLevel')
    extra_level = simple_property_reader.find_int_property(data, 'ExtraCharacterLevel')
    base_level = simple_property_reader.find_int_property(data, 'BaseCharacterLevel')
    status_extra = simple_property_reader.find_int_property(data, 'CharacterStatusComponent_ExtraCharacterLevel')
    status_base = simple_property_reader.find_int_property(data, 'CharacterStatusComponent_BaseCharacterLevel')
    
    exp = simple_property_reader.find_float_property(data, 'CharacterStatusComponent_ExperiencePoints') or 0
    
    print(f'{char_name:20s}:')
    print(f'  ExperiencePoints: {exp:.2f}')
    print(f'  CharacterLevel: {char_level}')
    print(f'  PlayerLevel: {player_level}')
    print(f'  ExtraCharacterLevel: {extra_level}')
    print(f'  BaseCharacterLevel: {base_level}')
    print(f'  StatusComponent_Extra: {status_extra}')
    print(f'  StatusComponent_Base: {status_base}')
    print()
