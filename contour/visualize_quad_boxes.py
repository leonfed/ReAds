import shutil

import cv2
import numpy as np
import os


# удалить содержимое папки
shutil.rmtree('../test_data/quad_contours')
os.makedirs('../test_data/quad_contours')

files = os.listdir('../test_data/quad_output')
contours_files = list(map(lambda x: x.split('.')[0], files))
print(contours_files)

for filename in contours_files:
    print(filename)
    contour = np.load('../test_data/quad_output/%s.npy' % filename)
    contour = np.append(contour, [contour[0]], axis=0)
    contour = np.vectorize(lambda x: int(x))(contour)

    input_filename = filename + '.png' if filename.startswith('synthetic_') else filename + '.jpg'
    original_image = cv2.imread('../test_data/input/' + input_filename)

    cv2.drawContours(original_image, [contour], -1, (0, 255, 0), 3)
    cv2.imwrite('../test_data/quad_contours/%s.jpg' % filename, original_image)
