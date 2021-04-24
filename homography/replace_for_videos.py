import os
import shutil

import cv2
import numpy as np


# заменить баннер на одном кадре
def process(filename, image_path, input_path, contours_path, result_path):
    print(filename)

    img_banner = cv2.imread(image_path)
    corners_banner = np.array(
        [[0, 0], [0, img_banner.shape[0]], [img_banner.shape[1], img_banner.shape[0]], [img_banner.shape[1], 0]])

    # Читаем кадр видео
    img_dst = cv2.imread(input_path + filename + '.jpg')

    # Читаем углы баннера на кадре
    contour = np.load(contours_path + filename + '.npy')

    # сортируем углы по часовой стрелке
    min_sum = 10000
    x1, y1 = 0, 0

    min_diff = 10000
    x2, y2 = 0, 0

    max_sum = 0
    x3, y3 = 0, 0

    max_diff = 0.0
    x4, y4 = 0, 0

    for [x, y] in contour:
        summ = x + y
        diff = x - y
        if summ < min_sum:
            min_sum = summ
            x1, y1 = x, y
        if diff < min_diff:
            min_diff = diff
            x2, y2 = x, y
        if summ > max_sum:
            max_sum = summ
            x3, y3 = x, y
        if diff > max_diff:
            max_diff = diff
            x4, y4 = x, y

    corners_dst = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    # Вычисляем гомография
    h, status = cv2.findHomography(corners_banner, corners_dst)

    # Проецируем баннер
    img_out = cv2.warpPerspective(img_banner, h, (img_dst.shape[1], img_dst.shape[0]))

    # Удалить баннер, который надо заменить
    mask = np.ones(img_dst.shape[:2], dtype="uint8") * 255
    cv2.drawContours(mask, [corners_dst], -1, 0, -1)
    img_dst = cv2.bitwise_and(img_dst, img_dst, mask=mask)

    # Смержить изображения
    img_res = cv2.addWeighted(img_dst, 1, img_out, 1, 0.0)
    cv2.imwrite(result_path + filename + '.jpg', img_res)


# Замена баннера на кадрах видео
if __name__ == "__main__":
    # путь до баннера, который нужно вставить
    image_path = '../video/data/banner.jpg'

    # путь до контуров
    contours_path = '../video/data/average_contours/'

    # путь до кадров
    input_path = '../video/data/input/'

    # путь до директории, куда нужно поместить кадры с замененным баннером
    result_path = '../video/data/processed_images/'

    # удалить содержимое директории
    # shutil.rmtree(result_path)
    # os.makedirs(result_path)

    files = os.listdir(contours_path)
    files = list(map(lambda x: x.split('.')[0], files))

    for filename in files:
        process(filename, image_path, input_path, contours_path, result_path)
