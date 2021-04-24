import cv2
import numpy as np

# Скрипт для замены баннера на одном изображении (с ручным указанием углов)
if __name__ == "__main__":
    # путь до баннера
    banner_path = '../images/25.jpg'

    # путь до изображения, в котором нужно банннер заменить
    image_path = '../test_data/input/129.jpg'

    # путь куда нужно записать результат замены
    result_path = 'example.jpg'

    # прочитать баннер
    img_banner = cv2.imread(banner_path)

    # ключевые точки баннера (углы)
    corners_banner = np.array(
        [[0, 0], [img_banner.shape[1], 0], [img_banner.shape[1], img_banner.shape[0]], [0, img_banner.shape[0]]])

    # прочитать углы изображения
    img_dst = cv2.imread(image_path)

    # указать углы на изображения
    [x1, y1, x2, y2, x3, y3, x4, y4] = [702, 100, 920, 106, 922, 215, 705, 215]
    corners_dst = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    # вычислить матрицу гомографии
    h, status = cv2.findHomography(corners_banner, corners_dst)

    # Спроецировать баннер
    img_out = cv2.warpPerspective(img_banner, h, (img_dst.shape[1], img_dst.shape[0]))

    # Удалить баннер, который надо заменить
    mask = np.ones(img_dst.shape[:2], dtype="uint8") * 255
    cv2.drawContours(mask, [corners_dst], -1, 0, -1)
    img_dst = cv2.bitwise_and(img_dst, img_dst, mask=mask)

    # Смержить изображения
    img_res = cv2.addWeighted(img_dst, 1, img_out, 1, 0.0)
    cv2.imwrite(result_path, img_res)
