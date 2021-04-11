import math
from random import randint

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from contour.utils import find_max_contour, to_rgb, find_intersection

filename = '555'
print(filename)

# читаем как черно-белое
img = cv2.imread('source/%s.jpg' % filename, cv2.IMREAD_GRAYSCALE)
# преобразование для сглаживания
# kernel = np.ones((9,9),np.uint8)
# img = cv2.dilate(img, kernel)
# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
# img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
edges = cv2.Canny(img, 20, 600, None, 3)

edges_img = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
cv2.imwrite('tmp2.jpg', edges_img)

# находим линии на контуре
linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 40, None, 40, 10)

original_path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
original_image = cv2.imread(original_path)

masks = np.load('masks/%s.npy' % filename)
scores = np.load('masks/scores_%s.npy' % filename)

# ищем контуры
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

print("Mask size: ", len(masks))

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
    permissible_distance = -np.sqrt(mask_area) / 6.0
    filtered_lines = []
    for i in range(0, len(linesP)):
        x1, y1, x2, y2 = linesP[i][0]

        # фильтруем линии. Оставляем те, которые близко к баннеру и достаточно длинные
        line_length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        dist1 = cv2.pointPolygonTest(max_contour, (x1, y1), True)
        dist2 = cv2.pointPolygonTest(max_contour, (x2, y2), True)
        if line_length < limit_line_length or dist1 < permissible_distance or dist2 < permissible_distance:
            continue
        filtered_lines.append(linesP[i][0])

    # рисуем найденные линии на изображении
    original_image_for_lines = cv2.imread(original_path)
    for line in filtered_lines:
        x1, y1, x2, y2 = line
        c = np.array([[x1, y1], [x2, y2]])
        cv2.drawContours(original_image_for_lines, [c], -1, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.imwrite('tmp3.jpg', original_image_for_lines)

    # рисуем линии по отдельности (для дебага)
    # for i in range(len(filtered_lines)):
    #     original_image_t = cv2.imread(original_path)
    #     c = np.array([filtered_lines[i][0:2], filtered_lines[i][2:4]])
    #     cv2.drawContours(original_image_t, [c], -1, (0, 255, 0), 3)
    #     cv2.imwrite('line_%i.jpg' % i, original_image_t)

    # найдем контуры и сравним их площадь с площадью маски
    print("Lines size: ", len(filtered_lines))
    contours_with_areas_coef = []
    for i1 in range(len(filtered_lines)):
        print("Current first line: ", i1)
        for i2 in range(i1 + 1, len(filtered_lines)):
            for i3 in range(i2 + 1, len(filtered_lines)):
                for i4 in range(i3 + 1, len(filtered_lines)):
                    line1 = filtered_lines[i1]
                    line2 = filtered_lines[i2]
                    line3 = filtered_lines[i3]
                    line4 = filtered_lines[i4]


                    def add_contour(l1, l2, l3, l4):
                        point1 = find_intersection(l1, l2)
                        point2 = find_intersection(l2, l3)
                        point3 = find_intersection(l3, l4)
                        point4 = find_intersection(l4, l1)
                        if any(p is None for p in [point1, point2, point3, point4]):
                            return
                        dist1 = cv2.pointPolygonTest(max_contour, (point1[0], point1[1]), True)
                        dist2 = cv2.pointPolygonTest(max_contour, (point2[0], point2[1]), True)
                        dist3 = cv2.pointPolygonTest(max_contour, (point3[0], point3[1]), True)
                        dist4 = cv2.pointPolygonTest(max_contour, (point4[0], point4[1]), True)
                        if any(d < permissible_distance for d in [dist1, dist2, dist3, dist4]):
                            return
                        c = np.array([point1, point2, point3, point4, point1])
                        coeff = abs(mask_area - cv2.contourArea(c))
                        contours_with_areas_coef.append((coeff, c))


                    add_contour(line1, line2, line3, line4)
                    add_contour(line1, line2, line4, line3)
                    add_contour(line1, line3, line2, line4)

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

    # выведем контуры в разные изображения (для дебага)
    # for i in range(len(candidates_contours)):
    #     original_image_t = cv2.imread(original_path)
    #     cv2.drawContours(original_image_t, [candidates_contours[i]], -1, (0, 255, 0), 3)
    #     cv2.imwrite('contours_%i.jpg' % i, original_image_t)

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

    print("Candidates score: ", candidates_score)

    # выбираем наилучший контур
    max_index = 0
    max_score = candidates_score[0]
    for c in range(len(candidates_contours)):
        if candidates_score[c] > max_score:
            max_score = candidates_score[c]
            max_index = c

    print("Max index: ", max_index)

    # рисуем наилучший контур
    cv2.drawContours(original_image, [candidates_contours[max_index]], -1, (0, 255, 0), 3)

cv2.imwrite('contours.jpg', original_image)
