from random import randint

import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from contour.utils import find_max_contour, to_rgb

filename = '275'
print(filename)

img = cv2.imread('source/%s.jpg' % filename, 0)
# преобразование для сглаживания
# kernel = np.ones((9,9),np.uint8)
# img = cv2.dilate(img, kernel)
# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
# img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
edges = cv2.Canny(img, 0, 100)

plt.imshow(edges, cmap='gray')
plt.savefig('tmp3.jpg')

path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
original_image = cv2.imread(path)

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
    black_white_image = np.array([[to_rgb(c) for c in r] for r in matrix])
    im = Image.fromarray(np.uint8(black_white_image))
    im.save('tmp.jpg')

    tmp_image = cv2.imread('tmp.jpg')

    im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
    im_bw = cv2.Canny(blur, 10, 90)
    matrix_contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # вычисляем площадь маски
    max_contour = find_max_contour(matrix_contours)
    mask_area = cv2.contourArea(max_contour)

    for c in contours:
        area = cv2.contourArea(c)
        scale = area / mask_area
        if 0.9 < scale < 1.1:
            cv2.drawContours(original_image, [c], -1, (randint(0, 255), randint(0, 255), randint(0, 255)), 3)

    cv2.imwrite('contours.jpg', original_image)
    exit()
