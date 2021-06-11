import os
import shutil

import cv2
import numpy as np

from utils.corners import sort_contour


# заменить баннер на одном кадре
def process(filename, image_path, input_path, contours_path, result_path, masks_path):
    print(filename)

    img_banner = cv2.imread(image_path)
    corners_banner = np.array(
        [[0, 0], [0, img_banner.shape[0]], [img_banner.shape[1], img_banner.shape[0]], [img_banner.shape[1], 0]])

    # Читаем кадр видео
    img_dst = cv2.imread(input_path + filename + '.jpg')

    # Читаем и сортируем углы баннера на кадре
    contour = np.load(contours_path + filename + '.npy')
    corners_dst = sort_contour(contour)

    # Вычисляем гомография
    h, status = cv2.findHomography(corners_banner, corners_dst)

    # Проецируем баннер
    img_out = cv2.warpPerspective(img_banner, h, (img_dst.shape[1], img_dst.shape[0]))

    # Удалить баннер, который надо заменить, но оставить человека перед баннером
    mask = cv2.imread(masks_path + filename + ".png", cv2.IMREAD_GRAYSCALE)

    for i in range(len(mask)):
        for j in range(len(mask[0])):
            dist = cv2.pointPolygonTest(contour, (j, i), True)
            if dist >= -1.0:
                if mask[i][j] <= 200:
                    img_dst[i][j] = np.array([0, 0, 0])
                else:
                    img_out[i][j] = np.array([0, 0, 0])


    # Смержить изображения
    img_res = cv2.addWeighted(img_dst, 1, img_out, 1, 0.0)
    cv2.imwrite(result_path + filename + '.jpg', img_res)


# Замена баннера на кадрах видео
if __name__ == "__main__":
    # путь до баннера, который нужно вставить
    image_path = '../video/data/banner_v2.jpg'

    # путь до контуров
    contours_path = '../video/data/contours/'

    # путь до кадров
    input_path = '../video/data/input/'

    # путь до карты глубины
    masks_path = '../video/data/people_masks/'

    # путь до директории, куда нужно поместить кадры с замененным баннером
    result_path = '../video/data/processed_images/'

    files_size = len(os.listdir(contours_path))

    for t in range(files_size):
        filename = str(t)
        process(filename, image_path, input_path, contours_path, result_path, masks_path)
