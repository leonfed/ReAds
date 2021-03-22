import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

filename = '22'

img = cv2.imread('source/%s.jpg' % filename)
edges = cv2.Canny(img, 50, 100)

# print(edges)
plt.imshow(edges, cmap='gray')
plt.savefig('contours.jpg')