import cv2
import numpy as np
from matplotlib import pyplot as plt


# Harris Corner Detection
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_features_harris/py_features_harris.html
def harris_corner_detection(input_file, result_file):
    img = cv2.imread(input_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    dst = cv2.dilate(dst, None)

    img[dst > 0.01 * dst.max()] = [0, 0, 255]

    cv2.imwrite(result_file, img)


# Shi-Tomasi Corner Detector
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_shi_tomasi/py_shi_tomasi.html
def shi_tomasi_corner_detection(input_file, result_file):
    img = cv2.imread(input_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    max_corners = 1000

    corners = cv2.goodFeaturesToTrack(gray, max_corners, 0.01, 10)
    corners = np.int0(corners)

    for i in corners:
        x, y = i.ravel()
        cv2.circle(img, (x, y), 3, 255, -1)

    plt.imshow(img, cmap='gray')
    plt.savefig(result_file)


# Определяет углы на изображении
if __name__ == "__main__":
    file = '../video/data/input/122.jpg'
    harris_corner_detection(file, 'contour.jpg')
