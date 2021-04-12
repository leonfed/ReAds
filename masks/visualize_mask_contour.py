import shutil

import cv2
import numpy as np
from PIL import Image
import os


def to_rgb(mask_value):
    return (0., 0., 0.) if mask_value else (255., 255., 255.)


# удалить содержимое папки
shutil.rmtree('../test_data/masks_raw_contours')
os.makedirs('../test_data/masks_raw_contours')

masks_files = os.listdir('../test_data/masks')
print(masks_files)

for raw_filename in masks_files:
    filename = raw_filename.split('.')[0]
    print(filename)

    mask = np.load('../test_data/masks/' + raw_filename)

    input_filename = filename + '.png' if filename.startswith('synthetic_') else filename + '.jpg'
    original_image = cv2.imread('../test_data/input/' + input_filename)

    black_white_image = np.array([[to_rgb(c) for c in r] for r in mask])
    im = Image.fromarray(np.uint8(black_white_image))
    im.save('tmp.jpg')

    tmp_image = cv2.imread('tmp.jpg')
    im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
    im_bw = cv2.Canny(blur, 10, 90)
    contours, _ = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # аппроксимируем четырехугольником
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) > 0:
            cv2.drawContours(original_image, [approx], -1, (0, 255, 0), 3)

    cv2.imwrite('../test_data/masks_raw_contours/%s.jpg' % filename, original_image)
