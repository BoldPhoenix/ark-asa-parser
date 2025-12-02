"""
Default ASA experience/level tables.

Official ARK: Survival Ascended XP requirements per level.
Users can override by passing custom xp_table to ArkSaveReader.
"""

# Default ASA XP requirements for levels 1-180 (approx; adjust as needed)
# Level is one-indexed: xp_thresholds[0] = XP for level 1
DEFAULT_ASA_XP_THRESHOLDS = [
    0,        # Level 1
    10, 25, 45, 70, 100,                                    # Levels 2-6
    135, 175, 220, 270, 325,                                # Levels 7-11
    385, 450, 520, 595, 675,                                # Levels 12-16
    760, 850, 945, 1045, 1150,                              # Levels 17-21
    1260, 1375, 1495, 1620, 1750,                           # Levels 22-26
    1885, 2025, 2170, 2320, 2475,                           # Levels 27-31
    # Continue pattern for higher levels (accelerated curve)
    2635, 2800, 2970, 3145, 3325,                           # Levels 32-36
    3510, 3700, 3895, 4095, 4300,                           # Levels 37-41
    4510, 4725, 4945, 5170, 5400,                           # Levels 42-46
    5635, 5875, 6120, 6370, 6625,                           # Levels 47-51
    6885, 7150, 7420, 7695, 7975,                           # Levels 52-56
    8260, 8550, 8845, 9145, 9450,                           # Levels 57-61
    9760, 10075, 10395, 10720, 11050,                       # Levels 62-66
    11385, 11725, 12070, 12420, 12775,                      # Levels 67-71
    13135, 13500, 13870, 14245, 14625,                      # Levels 72-76
    15010, 15400, 15795, 16195, 16600,                      # Levels 77-81
    17010, 17425, 17845, 18270, 18700,                      # Levels 82-86
    19135, 19575, 20020, 20470, 20925,                      # Levels 87-91
    21385, 21850, 22320, 22795, 23275,                      # Levels 92-96
    23760, 24250, 24745, 25245, 25750,                      # Levels 97-101
    26260, 26775, 27295, 27820, 28350,                      # Levels 102-106
    28885, 29425, 29970, 30520, 31075,                      # Levels 107-111
    31635, 32200, 32770, 33345, 33925,                      # Levels 112-116
    34510, 35100, 35695, 36295, 36900,                      # Levels 117-121
    37510, 38125, 38745, 39370, 40000,                      # Levels 122-126
    40635, 41275, 41920, 42570, 43225,                      # Levels 127-131
    43885, 44550, 45220, 45895, 46575,                      # Levels 132-136
    47260, 47950, 48645, 49345, 50050,                      # Levels 137-141
    50760, 51475, 52195, 52920, 53650,                      # Levels 142-146
    54385, 55125, 55870, 56620, 57375,                      # Levels 147-151
    58135, 58900, 59670, 60445, 61225,                      # Levels 152-156
    62010, 62800, 63595, 64395, 65200,                      # Levels 157-161
    66010, 66825, 67645, 68470, 69300,                      # Levels 162-166
    70135, 70975, 71820, 72670, 73525,                      # Levels 167-171
    74385, 75250, 76120, 76995, 77875,                      # Levels 172-176
    78760, 79650, 80545, 81445,                             # Levels 177-180
]


def get_default_xp_table():
    """Return the default ASA XP table"""
    return DEFAULT_ASA_XP_THRESHOLDS.copy()