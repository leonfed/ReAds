import colormath
import math


def euclid(rgb1, rgb2):
    (r1, g1, b1) = rgb1
    (r2, g2, b2) = rgb2
    distance = math.sqrt((r2 - r1) ** 2 + (b2 - b1) ** 2 + (b2 - b1) ** 2)
    # print(str(rgb1) + " ~ " + str(rgb2) + " = " + str(distance))
    return distance < 7.5


# see https://stackoverflow.com/questions/8863810/python-find-similar-colors-best-way
def stackoverflow_distance(rgb1, rgb2):
    (r1, g1, b1) = rgb1
    (r2, g2, b2) = rgb2
    rmean = (r1 + r2) / 2.0
    rd = r1 - r2
    gd = g1 - g2
    bd = b1 - b2
    sqr_distance = (512.0 + rmean) * rd * rd / 256.0 + 4.0 * gd * gd + (767.0 - rmean) * bd * bd / 256.0
    distance = math.sqrt(sqr_distance)
    # print(str(rgb1) + " ~ " + str(rgb2) + " = " + str(distance))
    return distance < 11.0


def is_similar_color(rgb1, rgb2):
    return euclid(rgb1, rgb2)
    # return stackoverflow_distance(rgb1, rgb2)
