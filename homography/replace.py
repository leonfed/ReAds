import cv2
import numpy as np

from utils.corners import sort_contour


# заменить баннер на одном кадре
def replace_banner(banner_path, input_path, contour_path, result_path):
    img_banner = cv2.imread(banner_path)
    corners_banner = np.array(
        [[0, 0], [0, img_banner.shape[0]], [img_banner.shape[1], img_banner.shape[0]], [img_banner.shape[1], 0]])

    # Читаем кадр видео
    img_dst = cv2.imread(input_path)

    # Читаем и сортируем углы баннера на кадре
    contour = np.load(contour_path)
    corners_dst = sort_contour(contour)

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
    cv2.imwrite(result_path, img_res)


# Скрипт для замены баннера на одном изображении (с ручным указанием углов)
if __name__ == "__main__":
    contour = np.array([[716, 473],
                        [713, 577],
                        [997, 553],
                        [1002, 457],
                        [716, 473]])

    # путь до баннера
    banner_path = 'banner.jpg'

    # путь до изображения, в котором нужно банннер заменить
    input_path = 'input.jpg'

    # путь куда нужно записать результат замены
    result_path = 'result.jpg'

    contour_path = 'contour.npy'
    np.save(contour_path, contour)
    replace_banner(banner_path, input_path, contour_path, result_path)
