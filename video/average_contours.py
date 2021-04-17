import shutil

import cv2
import os
from PIL import Image
import numpy as np

# удалить содержимое папки
shutil.rmtree('data/average_contours')
os.makedirs('data/average_contours')

files_count = len(os.listdir('data/final_result'))
print(files_count)


def find_points(contour):
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

    return [x1, y1, x2, y2, x3, y3, x4, y4]


all_points = []

for i in range(files_count):
    raw_contour = np.load('data/contours_fixed/%s.npy' % i)
    all_points.append(find_points(raw_contour))

def average_point(points):
    answer = []
    for i in range(len(points[0])):
        all = list(map(lambda x: x[i], points))
        p = sum(all) / len(points)
        answer.append(int(p))
    return answer


window = 10

for i in range(window, files_count - window):
    left = max(0, i - window)
    right = min(files_count, i + window)
    [x1, y1, x2, y2, x3, y3, x4, y4] = average_point(all_points[left:right])
    for_save = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])
    np.save('data/average_contours/%s' % i, for_save)

print("Ok")