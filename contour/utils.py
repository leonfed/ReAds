import cv2
import numpy as np
from PIL import Image
import os
from collections import deque
from shapely.geometry import LineString, Point


def to_rgb(mask_value):
    return (0., 0., 0.) if mask_value else (255., 255., 255.)


# находим контур с максимальной площадью
def find_max_contour(contours):
    max_index = 0
    max_area = cv2.contourArea(contours[0])
    for i in range(2, len(contours)):
        area = cv2.contourArea(contours[i])
        if area > max_area:
            max_area = area
            max_index = i

    return contours[max_index]


def line_formula(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0] * p2[1] - p2[0] * p1[1])
    return A, B, -C


def find_intersection(line1, line2):
    L1 = line_formula(line1[0:2], line1[2:4])
    L2 = line_formula(line2[0:2], line2[2:4])
    if L1 == L2:
        return None
    D = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return [int(x), int(y)]
    else:
        return None
