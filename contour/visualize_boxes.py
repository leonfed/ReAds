import shutil

import cv2
import numpy as np
import os


def process(filename, contour_path, image_path, result_path):
    print(filename)
    contour = np.load(contour_path + filename + '.npy')
    contour = np.append(contour, [contour[0]], axis=0)
    contour = np.vectorize(lambda x: int(x))(contour)

    input_filename = filename + '.png' if filename.startswith('synthetic_') else filename + '.jpg'
    original_image = cv2.imread(image_path + input_filename)

    cv2.drawContours(original_image, [contour], -1, (0, 255, 0), 3)
    cv2.imwrite(result_path + filename + '.jpg', original_image)


# Рисует контуры
if __name__ == "__main__":
    contour_path = '../video/data_4/voodoo_contours/'
    image_path = '../video/data_4/input/'
    result_path = '../video/data_4/voodoo_contours_images/'

    files = os.listdir(contour_path)
    contours_files = list(map(lambda x: x.split('.')[0], files))
    print(contours_files)
    for filename in contours_files:
        process(filename, contour_path, image_path, result_path)
