import math
from random import randint

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from contour.utils import find_max_contour, to_rgb, find_intersection

filename = '339'
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
    height = len(matrix)
    width = len(matrix[0])

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
    print("Mask area: ", mask_area)

    # фильтруем найденные линии
    limit_line_length = np.sqrt(mask_area) / 4.0
    permissible_distance = np.sqrt(mask_area) / 4.0
    filtered_lines = []
    for i in range(0, len(linesP)):
        x1, y1, x2, y2 = linesP[i][0]

        # фильтруем линии. Оставляем те, которые близко к баннеру и достаточно длинные
        line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        dist1 = cv2.pointPolygonTest(max_contour, (x1, y1), True)
        dist2 = cv2.pointPolygonTest(max_contour, (x2, y2), True)
        if line_length < limit_line_length or dist1 < -permissible_distance or dist2 < -permissible_distance:
            continue
        filtered_lines.append(linesP[i][0])

    # рисуем найденные линии на изображении
    original_image_for_lines = cv2.imread(original_path)
    for line in filtered_lines:
        x1, y1, x2, y2 = line
        c = np.array([[x1, y1], [x2, y2]])
        cv2.drawContours(original_image_for_lines, [c], -1, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.imwrite('tmp3.jpg', original_image_for_lines)

    # найдем контуры и сравним их площадь с площадью маски
    print("Lines size: ", len(filtered_lines))
    contours_with_areas_coef = []
    for i1 in range(len(filtered_lines)):
        print("Current first line: ", i1)
        line1 = filtered_lines[i1]

        for i2 in range(i1 + 1, len(filtered_lines)):
            line2 = filtered_lines[i2]
            point1 = find_intersection(line1, line2, height, width)
            if point1 == None or (line1 == line2).all():
                continue

            for i3 in range(i2 + 1, len(filtered_lines)):
                line3 = filtered_lines[i3]
                point2 = find_intersection(line2, line3, height, width)
                if point2 == None or (line3 == line1).all() or (line3 == line2).all():
                    continue

                for i4 in range(i3 + 1, len(filtered_lines)):
                    line4 = filtered_lines[i4]
                    point3 = find_intersection(line3, line4, height, width)
                    if point3 == None:
                        continue
                    point4 = find_intersection(line4, line1, height, width)
                    if point4 == None:
                        continue
                    if (line4 == line1).all() or (line4 == line2).all() or (line4 == line3).all():
                        continue


                    def add_contour(c):
                        coeff = abs(mask_area - cv2.contourArea(c))
                        contours_with_areas_coef.append((coeff, c))


                    add_contour(np.array([point1, point2, point3, point4, point1]))
                    add_contour(np.array([point1, point2, point4, point3, point1]))
                    add_contour(np.array([point1, point3, point2, point4, point1]))

    # сортируем
    contours_with_areas_coef = sorted(contours_with_areas_coef, key=lambda x: x[0])
    print("Contours size: ", len(contours_with_areas_coef))
    candidates_contours = list(map(lambda t: t[1], contours_with_areas_coef[0:11]))
    candidates_score = [0 for _ in candidates_contours]

    if len(candidates_contours) == 0:
        continue

    # рисуем найденные кандидиаты
    original_image_for_candidates = cv2.imread(original_path)
    for c in candidates_contours:
        cv2.drawContours(original_image_for_candidates, [c], -1, (randint(0, 255), randint(0, 255), randint(0, 255)), 3,
                         cv2.LINE_AA)
    cv2.imwrite('tmp4.jpg', original_image_for_candidates)

    # считаем score пересечения контура и маски
    print("Matrix: %s" % str(len(matrix)))
    for i in range(len(matrix)):
        print("Matrix index: %s" % str(i))
        for j in range(len(matrix[0])):
            for c in range(len(candidates_contours)):
                contour = candidates_contours[c]
                dist = cv2.pointPolygonTest(contour, (j, i), True)
                if matrix[i][j] and dist >= 0.0:
                    candidates_score[c] += 1
                if not matrix[i][j] and dist >= 0.0:
                    candidates_score[c] -= 1

    # выбираем наилучший контур
    max_index = 0
    max_score = candidates_score[0]
    for c in range(len(candidates_contours)):
        if candidates_score[c] > max_score:
            max_score = candidates_score[c]
            max_index = c

    # рисуем наилучший контур
    cv2.drawContours(original_image, [candidates_contours[max_index]], -1, (0, 255, 0), 3)

cv2.imwrite('contours.jpg', original_image)
