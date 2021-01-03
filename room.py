names = [
    "apartment_2", # not enough, but it's hard to create these
    "office_1", # skip it because colors
    "office_2", # ready
    "apartment_1", # ready
    "frl_apartment_0",
    "frl_apartment_1",
    "office_0"
]

wall_indexes = [
    [190, 76, 58, 55, 54, 14, 21, 12, 40, 18, 33, 20, 150, 165, 90, 99, 110, 134],
    [49, 46, 53, 27, 33],
    [19, 60, 71, 63],
    [100, 98, 96, 35, 46, 50, 55, 78],
    [222, 212, 26, 14, 50, 9, 6, 87, 128, 100, 114, 117, 142, 162],
    [172, 168, 57, 5, 4, 28, 29, 23, 87, 88, 92, 100, 118, 129, 132, 148],
    [51, 18, 8, 26, 24]
]


def get_room(i):
    return names[i], wall_indexes[i]
