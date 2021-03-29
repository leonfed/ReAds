import cv2
import numpy as np

# synthetic_16
# Координаты контура
# [[[981  54]]
#  [[701  86]]
#  [[683 481]]
#  [[962 502]]]


# Read source image.
img_src = cv2.imread('for_replace.jpg')
print(img_src.shape)
# Four corners of the book in source image
corners_src = np.array([[0, 0], [img_src.shape[1], 0], [img_src.shape[1], img_src.shape[0]], [0, img_src.shape[0]]])

# Read destination image.
img_dst = cv2.imread('synthetic_16.jpg')
# Four corners of the book in destination image.
corners_dst = np.array([[701, 86], [981, 54], [962, 502], [683, 481]])

# Calculate Homography
h, status = cv2.findHomography(corners_src, corners_dst)

# Warp source image to destination based on homography
img_out = cv2.warpPerspective(img_src, h, (img_dst.shape[1], img_dst.shape[0]))

# Удалить баннер, который надо заменить
mask = np.ones(img_dst.shape[:2], dtype="uint8") * 255
cv2.drawContours(mask, [corners_dst], -1, 0, -1)
img_dst = cv2.bitwise_and(img_dst, img_dst, mask=mask)

# Смержить изображения
img_res = cv2.addWeighted(img_dst, 1, img_out, 1, 0.0)
cv2.imwrite("result.jpg", img_res)
