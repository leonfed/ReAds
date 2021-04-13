import math

import cv2
import numpy as np
from PIL import Image
import os
from collections import deque

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


class DFS:
    def __init__(self, image_pix, selected_pixels, points, banner_area, distance):
        self.image_pix = image_pix
        self.selected_pixels = selected_pixels
        self.points = points
        self.distance = distance
        self.height = len(self.selected_pixels)
        self.width = len(self.selected_pixels[0])
        self.banner_area = banner_area
        self.completed = True

    def euclid(self, rgb1, rgb2):
        (r1, g1, b1) = rgb1
        (r2, g2, b2) = rgb2
        distance = math.sqrt((r2 - r1) ** 2 + (b2 - b1) ** 2 + (b2 - b1) ** 2)
        return distance < self.distance

    def dfs_draw(self):
        while len(self.points) > 0:
            if len(self.points) > self.banner_area * 3:
                self.completed = False
                break

            (x, y) = self.points.pop()
            current_pixel = self.image_pix[y, x]
            for i in range(x - 2, x + 3):
                for j in range(y - 2, y + 3):
                    if i < 0 or j < 0 or i >= self.height or j >= self.width:
                        continue
                    if self.selected_pixels[i][j]:
                        continue
                    if self.euclid(current_pixel, self.image_pix[j, i]):
                        self.selected_pixels[i][j] = True
                        self.points.append((i, j))


files = os.listdir('../test_data/masks')
masks_files = list(map(lambda x: x.split('.')[0], files))
print(masks_files)

masks_files = ['synthetic_4']

for filename in masks_files:
    print(filename)
    mask = np.load('../test_data/masks/%s.npy' % filename)

    # читаем оригинальное изображение
    input_filename = filename + '.png' if filename.startswith('synthetic_') else filename + '.jpg'
    path = "../test_data/input/" + input_filename
    image = Image.open(path)
    image_width = image.size[0]
    image_height = image.size[1]
    image_pix = image.load()
    original_image = cv2.imread(path)

    # находим контур маски
    black_white_image = np.array([[to_rgb(c) for c in r] for r in mask])
    im = Image.fromarray(np.uint8(black_white_image))
    im.save('tmp.jpg')

    tmp_image = cv2.imread('tmp.jpg')
    im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
    im_bw = cv2.Canny(blur, 10, 90)
    contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # определяем максимальный контур и уменьшаем его
    max_contour = find_max_contour(contours)
    scaled_contour = scale_contour(max_contour)

    # массив пикселей, которые отнесены к баннеру
    selected_pixels = np.zeros((image_height, image_width), dtype=bool)

    started_points = deque()

    mask_area = 0

    for i in range(len(selected_pixels)):
        for j in range(len(selected_pixels[0])):
            dist = cv2.pointPolygonTest(scaled_contour, (j, i), False)
            if mask[i][j] and dist >= 0.0:
                selected_pixels[i][j] = True
                started_points.append((i, j))
                mask_area += 1

    # бинпоиск чтобы найти оптимальное расстояние
    eps = 0.001
    left = 0.01
    right = 50
    result_pixels = selected_pixels.copy()
    while right - left > eps:
        print(left, right)
        middle = (right + left) / 2
        dfs = DFS(image_pix, selected_pixels.copy(), started_points.copy(), mask_area, middle)
        dfs.dfs_draw()
        if dfs.completed:
            left = middle
            result_pixels = dfs.selected_pixels
        else:
            right = middle

    # определяем финальный контур
    black_white_image = np.array([[to_rgb(c) for c in r] for r in result_pixels])
    im = Image.fromarray(np.uint8(black_white_image))
    im.save('tmp2.jpg')
    tmp_image = cv2.imread('tmp2.jpg')
    im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
    im_bw = cv2.Canny(blur, 10, 90)
    contours, _ = cv2.findContours(im_bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        print("Skip because contours not found")
    max_contour = find_max_contour(contours)
    peri = cv2.arcLength(max_contour, True)

    # немного апроксимируем
    approx = cv2.approxPolyDP(max_contour, 0.02 * peri, True)

    for_save = np.array([t[0] for t in approx])
    print(for_save)

    if len(for_save) < 4:
        print("Skip image because contour is not found")
    else:
        cv2.drawContours(original_image, [approx], -1, (0, 255, 0), 3)
        cv2.imwrite('contour.jpg', original_image)

    print('\n')
