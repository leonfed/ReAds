from random import randint

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

filename = '275'

img = cv2.imread('source/%s.jpg' % filename, 0)
edges = cv2.Canny(img, 0, 100)

# print(edges)
plt.imshow(edges, cmap='gray')
plt.savefig('tmp.jpg')

# ищем контуры
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# запомимаем четрехугольные контуры
quadrilateral_contours = []
contours_score = []
for c in contours:
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    if len(approx) == 4 and cv2.contourArea(approx) > 100.0:
        quadrilateral_contours.append(approx)
        contours_score.append(0)

print("quadrilateral_contours: %s" % len(quadrilateral_contours))

path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
masks = np.load('examples/%s.npy' % filename)
scores = np.load('examples/scores_%s.npy' % filename)

original_image = cv2.imread(path)

if len(masks) < 1:
    print("Empty masks")
    exit()

# убрать накладывающиеся
new_masks = [masks[0]]
new_scores = [scores[0]]


def is_intersection(mask1, mask2):
    count = 0
    all_count = 0
    for i in range(len(mask1)):
        for j in range(len(mask1[0])):
            if mask1[i][j]:
                all_count += 1
            if mask2[i][j]:
                all_count += 1
            if mask1[i][j] and mask2[i][j]:
                count += 1
    return count > all_count / 10


for i in range(len(masks)):
    is_added = False
    for j in range(len(new_masks)):
        if is_intersection(masks[i], new_masks[j]):
            is_added = True
            for x in range(len(new_masks[j])):
                for y in range(len(new_masks[j][0])):
                    if masks[i][x][y]:
                        new_masks[j][x][y] = True
            new_scores[j] = (new_scores[j] + scores[i]) / 2
    if not is_added:
        new_masks.append(masks[i])
        new_scores.append(scores[i])

masks = new_masks
scores = new_scores

# Перебираем маски
print("Masks: %s" % str(len(masks)))
for t in range(len(masks)):
    print("Masks index: %s" % str(t))
    if scores[t] < 0.9:
        continue
    matrix = masks[t]

    print("Matrix: %s" % str(len(matrix)))
    for i in range(len(matrix)):
        print("Matrix index: %s" % str(i))
        for j in range(len(matrix[0])):
            for c in range(len(quadrilateral_contours)):
                contour = quadrilateral_contours[c]
                dist = cv2.pointPolygonTest(contour, (j, i), True)
                if matrix[i][j] and dist >= 0.0:
                    contours_score[c] += 1
                if not matrix[i][j] and dist >= 0.0:
                    contours_score[c] -= 1

print(contours_score)

max_index = 0
max_score = contours_score[0]

for c in range(len(quadrilateral_contours)):
    if contours_score[c] > max_score:
        max_score = contours_score[c]
        max_index = c

print(max_index)
print(max_score)

cv2.drawContours(original_image, [quadrilateral_contours[max_index]], -1, (0, 255, 0), 3)
cv2.imwrite('contours.jpg', original_image)
