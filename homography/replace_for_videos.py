import os

from homography.replace import replace_banner

# Замена баннера на кадрах видео
if __name__ == "__main__":
    # путь до баннера, который нужно вставить
    image_path = '../video/data/banner.jpg'

    # путь до контуров
    contours_path = '../video/data/voodoo_contours/'

    # путь до кадров
    input_path = '../video/data/input/'

    # путь до директории, куда нужно поместить кадры с замененным баннером
    result_path = '../video/data/processed_images/'

    files = os.listdir(contours_path)
    files = list(map(lambda x: x.split('.')[0], files))

    for filename in files:
        replace_banner(image_path,
                       input_path + filename + '.jpg',
                       contours_path + filename + '.npy',
                       result_path + filename + '.jpg')
