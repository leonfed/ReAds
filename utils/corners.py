import numpy as np


# сортируем углы по часовой стрелке
def sort_contour(contour):
    min_sum = 10000
    x1, y1 = 0, 0

    min_diff = 10000
    x2, y2 = 0, 0

    max_sum = 0
    x3, y3 = 0, 0

    max_diff = 0.0
    x4, y4 = 0, 0

    for [x, y] in contour:
        summ = x + y
        diff = x - y
        if summ < min_sum:
            min_sum = summ
            x1, y1 = x, y
        if diff < min_diff:
            min_diff = diff
            x2, y2 = x, y
        if summ > max_sum:
            max_sum = summ
            x3, y3 = x, y
        if diff > max_diff:
            max_diff = diff
            x4, y4 = x, y

    result = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    return result
