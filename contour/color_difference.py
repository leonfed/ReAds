import colormath
import math


def is_similar_color(rgb1, rgb2):
    (r1, g1, b1) = rgb1
    (r2, g2, b2) = rgb2
    distance = math.sqrt((r2 - r1) ** 2 + (b2 - b1) ** 2 + (b2 - b1) ** 2)
    # print(str(rgb1) + " ~ " + str(rgb2) + " = " + str(distance))
    return distance < 3.0
