import os
import random
import shutil

import cv2
import numpy as np
import pandas

image_path = '../video/data/banner.jpg'

# удалить содержимое папки
shutil.rmtree('../video/data/processed_images')
os.makedirs('../video/data/processed_images')

files = os.listdir('../video/data/average_contours')
files = list(map(lambda x: x.split('.')[0], files))

for filename in files:
    print(filename)

    img_banner = cv2.imread(image_path)
    # Four corners of the book in banner image
    corners_banner = np.array(
        [[0, 0], [0, img_banner.shape[0]], [img_banner.shape[1], img_banner.shape[0]], [img_banner.shape[1], 0]])

    # Read destination image.
    img_dst = cv2.imread('../video/data/input/%s.jpg' % filename)

    # Four corners of the book in destination image.
    contour = np.load('../video/data/average_contours/%s.npy' % filename)
    # print(contour)

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

    # print(x1, y1)
    # print(x2, y2)
    # print(x3, y3)
    # print(x4, y4)

    corners_dst = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    # Calculate Homography
    h, status = cv2.findHomography(corners_banner, corners_dst)

    # Warp source image to destination based on homography
    img_out = cv2.warpPerspective(img_banner, h, (img_dst.shape[1], img_dst.shape[0]))

    # Удалить баннер, который надо заменить
    mask = np.ones(img_dst.shape[:2], dtype="uint8") * 255
    cv2.drawContours(mask, [corners_dst], -1, 0, -1)
    img_dst = cv2.bitwise_and(img_dst, img_dst, mask=mask)

    # Смержить изображения
    img_res = cv2.addWeighted(img_dst, 1, img_out, 1, 0.0)
    cv2.imwrite("../video/data/processed_images/%s.jpg" % filename, img_res)
