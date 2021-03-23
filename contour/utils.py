import cv2
import numpy as np
from PIL import Image
import os
from collections import deque


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
