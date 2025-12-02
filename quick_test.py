xp = 0
for level in range(2, 181):
    xp += 75 * (1.0015 ** level)
    if level in [50, 100, 127, 135, 150, 180]:
        print(f'Level {level}: {xp:,.0f} total XP')
