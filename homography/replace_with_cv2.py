import random

import cv2
import numpy as np
import pandas

all_corners = pandas.read_csv('corners.csv').values

vertical_images_name = ['41', '42']
horizontal_images_name = ['7']

for corners in all_corners:
    print('Corners: %s' % corners)
    [filename, x1, y1, x2, y2, x3, y3, x4, y4] = corners

    # Read banner
    if abs(x2 - x1) + abs(x3 - x2) < abs(y2 - y1) + abs(y3 - y2):
        banner_name = random.choice(vertical_images_name)
    else:
        banner_name = random.choice(horizontal_images_name)
    print("Banner name: %s" % banner_name)
    img_banner = cv2.imread('../images/%s.jpg' % banner_name)
    # Four corners of the book in banner image
    corners_banner = np.array([[0, 0], [img_banner.shape[1], 0], [img_banner.shape[1], img_banner.shape[0]], [0, img_banner.shape[0]]])

    # Read destination image.
    img_dst = cv2.imread('source/%s.jpg' % filename)
    # Four corners of the book in destination image.
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
    cv2.imwrite("cv2_results/%s.jpg" % filename, img_res)
