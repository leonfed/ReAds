from random import randint

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from contour.utils import to_rgb, find_max_contour

filename = 'synthetic_16'

img = cv2.imread('source/%s.jpg' % filename, 0)
kernel = np.ones((5,5),np.uint8)
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
edges = cv2.Canny(img, 0, 100)

# print(edges)
plt.imshow(edges, cmap='gray')
plt.savefig('tmp.jpg')

# ищем контуры
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# запомимаем четрехугольные контуры
quadrilateral_contours = []

for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4:
        quadrilateral_contours.append(approx)

print("quadrilateral_contours: %s" % len(quadrilateral_contours))

path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
masks = np.load('masks/%s.npy' % filename)
scores = np.load('masks/scores_%s.npy' % filename)

original_image = cv2.imread(path)

if len(masks) < 1:
    print("Empty masks")
    exit()

# Перебираем маски
print("Masks: %s" % str(len(masks)))
for t in range(len(masks)):
    print("Masks index: %s" % str(t))
    if scores[t] < 0.9:
        continue
    matrix = masks[t]

    # вычисляем площадь маски
    black_white_image = np.array([[to_rgb(c) for c in r] for r in matrix])
    im = Image.fromarray(np.uint8(black_white_image))
    im.save('tmp.jpg')
    tmp_image = cv2.imread('tmp.jpg')
    im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
    im_bw = cv2.Canny(blur, 10, 90)
    matrix_contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    max_contour = find_max_contour(matrix_contours)
    mask_area = cv2.contourArea(max_contour)

    current_contours = []
    contours_score = []

    for c in quadrilateral_contours:
        area = cv2.contourArea(c)
        scale = area / mask_area
        if 0.8 < scale < 1.2:
            current_contours.append(c)
            contours_score.append(0)

    print("current_contours: %s" % len(current_contours))

    if len(current_contours) == 0:
        continue

    print("Matrix: %s" % str(len(matrix)))
    for i in range(len(matrix)):
        print("Matrix index: %s" % str(i))
        for j in range(len(matrix[0])):
            for c in range(len(current_contours)):
                contour = current_contours[c]
                dist = cv2.pointPolygonTest(contour, (j, i), True)
                if matrix[i][j] and dist >= 0.0:
                    contours_score[c] += 1
                if not matrix[i][j] and dist >= 0.0:
                    contours_score[c] -= 1

    print(contours_score)

    max_index = 0
    max_score = contours_score[0]

    for c in range(len(current_contours)):
        if contours_score[c] > max_score:
            max_score = contours_score[c]
            max_index = c

    print(max_index)
    print(max_score)

    print(current_contours[max_index])

    cv2.drawContours(original_image, [current_contours[max_index]], -1, (0, 255, 0), 3)

cv2.imwrite('contours.jpg', original_image)
