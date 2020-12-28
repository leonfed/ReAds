names = [
    "apartment_2",
    "office_1",
    "office_2",
    "apartment_1"
]

wall_indexes = [
    [190, 76, 58, 55, 54, 14, 21, 12, 40, 18, 33, 20, 150, 165, 90, 99, 110, 134],
    [49, 46, 53, 27, 33],
    [19, 60, 71, 63],
    [100, 98, 96, 35, 46, 50, 55, 78]
]


def get_room(i):
    return names[i], wall_indexes[i]
