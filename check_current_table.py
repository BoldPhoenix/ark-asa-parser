from ark_asa_parser.levels import xp_to_level
from ark_asa_parser.xp_data import get_default_xp_table

table = get_default_xp_table()
xp = 28468720

level = xp_to_level(xp, xp_table=table)
print(f'XP in profile: {xp:,}')
print(f'Calculated level with current table: {level}')
print(f'Max level in table: {len(table)}')
print(f'XP required for level 180: {table[179] if len(table) > 179 else "N/A"}')
print(f'\nThis is why everyone shows as level 180 - the XP values exceed the table maximum!')
print(f'\nIn-game screenshot shows level 132, so the profile XP value must use')
print(f'a different system than the level-up XP table.')
