import cv2
import numpy as np
from PIL import Image
import os
from collections import deque

from contour.color_difference import is_similar_color
from contour.utils import to_rgb, find_max_contour


def scale_contour(contour):
    scale_coefficient = 0.90
    M = cv2.moments(contour)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

    cnt_norm = contour - [cx, cy]
    cnt_scaled = cnt_norm * scale_coefficient
    cnt_scaled = cnt_scaled + [cx, cy]
    cnt_scaled = cnt_scaled.astype(np.int32)

    return cnt_scaled


def dfs_draw(selected_pixels, image_pix, deque_points):
    while len(deque_points) > 0:
        (x, y) = deque_points.pop()
        current_pixel = image_pix[y, x]
        height = len(selected_pixels)
        width = len(selected_pixels[0])
        for i in range(x - 2, x + 3):
            for j in range(y - 2, y + 3):
                if i < 0 or j < 0 or i >= height or j >= width:
                    continue
                if selected_pixels[i][j]:
                    continue
                if is_similar_color(current_pixel, image_pix[j, i]):
                    selected_pixels[i][j] = True
                    deque_points.append((i, j))


all_files = os.listdir('masks')
filtered = filter(lambda x: x.endswith('npy') and not x.startswith('scores'), all_files)
masks_files = list(map(lambda x: x.split('.')[0], filtered))
print(masks_files)

# masks_files = masks_files[0:10]
# masks_files = [masks_files[10]]
# masks_files = [masks_files[40]]
masks_files = ['295']

for filename in masks_files:
    print(filename)
    masks = np.load('masks/%s.npy' % filename)
    scores = np.load('masks/scores_%s.npy' % filename)

    # читаем оригинальное изображение
    path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
    image = Image.open(path)
    image_width = image.size[0]
    image_height = image.size[1]
    image_pix = image.load()
    original_image = cv2.imread(path)

    # выделить контуры
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
        contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # определяем контур и уменьшаем его
        max_contour = find_max_contour(contours)
        cv2.drawContours(tmp_image, [max_contour], -1, (0, 255, 0), 3)
        scaled_contour = scale_contour(max_contour)
        cv2.drawContours(tmp_image, [scaled_contour], -1, (0, 0, 255), 3)

        # массив пикселей, которые отнесены к баннеру
        selected_pixels = np.zeros((image_height, image_width), dtype=bool)

        started_points = deque()

        for i in range(len(selected_pixels)):
            for j in range(len(selected_pixels[0])):
                dist = cv2.pointPolygonTest(scaled_contour, (j, i), False)
                if matrix[i][j] and dist >= 0.0:
                    selected_pixels[i][j] = True
                    started_points.append((i, j))

        dfs_draw(selected_pixels, image_pix, started_points)

        # определяем финальный контур
        black_white_image = np.array([[to_rgb(c) for c in r] for r in selected_pixels])
        im = Image.fromarray(np.uint8(black_white_image))
        im.save('tmp2_%s.jpg' % k)
        tmp_image = cv2.imread('tmp2_%s.jpg' % k)
        im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
        im_bw = cv2.Canny(blur, 10, 90)
        contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        max_contour = find_max_contour(contours)
        peri = cv2.arcLength(max_contour, True)
        approx = cv2.approxPolyDP(max_contour, 0.02 * peri, True)
        cv2.drawContours(original_image, [approx], -1, (0, 255, 0), 3)

    cv2.imwrite('by_color_results/%s.jpg' % filename, original_image)
