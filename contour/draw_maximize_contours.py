import os

import cv2
import numpy as np


def toInt(x):
    return int(x)


all_files = os.listdir('maximize_contours')
files = list(map(lambda x: x.split('.')[0], all_files))
print(files)

for filename in files:
    print(filename)
    path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
    contours = np.load('maximize_contours/%s.npy' % filename)
    contours = np.vectorize(toInt)(contours)

    original_image = cv2.imread(path)

    scores = np.load('masks/scores_%s.npy' % filename)

    for i in range(len(contours)):
        if scores[i] > 0.90:
            cv2.drawContours(original_image, [contours[i]], -1, (0, 255, 0), 3)

    cv2.imwrite('maximize_results/%s.jpg' % filename, original_image)
