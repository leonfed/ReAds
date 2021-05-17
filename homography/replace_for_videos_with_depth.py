import os
import shutil

import cv2
import numpy as np

from utils.corners import sort_contour


# заменить баннер на одном кадре
def process(filename, image_path, input_path, contours_path, result_path, depth_maps_path, max_depth):
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

    # Удалить баннер, который надо заменить
    # mask = np.ones(img_dst.shape[:2], dtype="uint8") * 255
    # cv2.drawContours(mask, [corners_dst], -1, 0, -1)
    # img_dst = cv2.bitwise_and(img_dst, img_dst, mask=mask)
    # print(img_dst[400][400])
    # print(img_out[400][400])

    depth_map = np.load(depth_maps_path + filename + ".npy")

    for i in range(len(depth_map)):
        for j in range(len(depth_map[0])):
            dist = cv2.pointPolygonTest(contour, (j, i), False)
            if dist >= 0.0:
                if depth_map[i][j] <= max_depth:
                    img_dst[i][j] = np.array([0, 0, 0])
                else:
                    img_out[i][j] = np.array([0, 0, 0])

    # Смержить изображения
    img_res = cv2.addWeighted(img_dst, 1, img_out, 1, 0.0)
    cv2.imwrite(result_path + filename + '.jpg', img_res)


def get_max_depth(contour, depth_map):
    max_depth = -10000.0
    for i in range(len(depth_map)):
        for j in range(len(depth_map[0])):
            dist = cv2.pointPolygonTest(contour, (j, i), False)
            if dist >= 0.0:
                max_depth = max(max_depth, depth_map[i][j])

    return max_depth


# Замена баннера на кадрах видео
if __name__ == "__main__":
    # путь до баннера, который нужно вставить
    image_path = '../video/data_4/banner.jpg'

    # путь до контуров
    contours_path = '../video/data_4/voodoo_contours/'

    # путь до кадров
    input_path = '../video/data_4/input/'

    # путь до карты глубины
    depth_maps_path = '../video/data_4/depth_maps/'

    # путь до директории, куда нужно поместить кадры с замененным баннером
    result_path = '../video/data_4/processed_images/'

    first_contour = np.load(contours_path + "0.npy")
    first_depth_map = np.load(depth_maps_path + "0.npy")
    max_depth = get_max_depth(first_contour, first_depth_map)
    max_depth = max_depth * 1.2

    files_size = len(os.listdir(contours_path))

    for t in range(files_size):
        filename = str(t)
        process(filename, image_path, input_path, contours_path, result_path, depth_maps_path, max_depth)
