import math
from random import randint

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from contour.utils import find_max_contour, to_rgb

filename = '295'
print(filename)

# читаем как черно-белое
img = cv2.imread('source/%s.jpg' % filename, cv2.IMREAD_GRAYSCALE)
# преобразование для сглаживания
# kernel = np.ones((9,9),np.uint8)
# img = cv2.dilate(img, kernel)
# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
# img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
edges = cv2.Canny(img, 50, 500, None, 3)

edges_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
cv2.imwrite('tmp2.jpg', edges_img)

# находим линии на контуре
linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, None, 50, 10)

original_path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
original_image = cv2.imread(original_path)

masks = np.load('masks/%s.npy' % filename)
scores = np.load('masks/scores_%s.npy' % filename)

# ищем контуры
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# перебираем маски
for k in range(len(masks)):
    # убираем то, в чем плохо уверены
    if scores[k] < 0.9:
        continue

    matrix = masks[k]

    # сохраняем область маски в tmp.jpg
    black_white_image = np.array([[to_rgb(c) for c in r] for r in matrix])
    im = Image.fromarray(np.uint8(black_white_image))
    im.save('tmp.jpg')

    # находим контур маски
    tmp_image = cv2.imread('tmp.jpg')
    im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
    im_bw = cv2.Canny(blur, 10, 90)
    matrix_contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # вычисляем площадь маски
    max_contour = find_max_contour(matrix_contours)
    mask_area = cv2.contourArea(max_contour)

    # рисуем найденные линии на изображении
    original_image_for_lines = cv2.imread(original_path)
    limit_line_length = np.sqrt(mask_area) / 4.0
    permissible_distance = np.sqrt(mask_area) / 4.0
    if linesP is not None:
        for i in range(0, len(linesP)):
            x1, y1, x2, y2 = linesP[i][0]

            # фильтруем линии. Оставляем те, которые близко к баннеру и достаточно длинные
            line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            dist1 = cv2.pointPolygonTest(max_contour, (x1, y1), True)
            dist2 = cv2.pointPolygonTest(max_contour, (x2, y2), True)
            if line_length < limit_line_length or dist1 < -permissible_distance or dist2 < -permissible_distance:
                continue

            c = np.array([[x1, y1], [x2, y2]])
            cv2.drawContours(original_image_for_lines, [c], -1, (0, 0, 255), 3, cv2.LINE_AA)

    cv2.imwrite('tmp3.jpg', original_image_for_lines)


    # выбираем подходящие контуры и рисуем их
    for c in contours:
        area = cv2.contourArea(c)
        scale = area / mask_area
        if 0.9 < scale < 1.1:
            cv2.drawContours(original_image, [c], -1, (randint(0, 255), randint(0, 255), randint(0, 255)), 3)

    cv2.imwrite('contours.jpg', original_image)

    # обрабатываем пока только одну маску
    exit()
