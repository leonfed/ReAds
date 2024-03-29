import pandas
import numpy as np
import sys
from PIL import Image
from io import BytesIO
import pathlib

from generation.utils import hex2rgb


def process_screenshot(data, raw_screenshots_path, result_path):
    [screenshot, special_screenshot, special_color, room, wall_index, image] = data

    print(screenshot)

    path = pathlib.Path(result_path + screenshot + '.png')
    if path.is_file():
        print("Path %s already exists\n" % path)
        return

    special_color_rbg = hex2rgb(special_color)

    # скриншот с вставленным баннером
    path_normal = raw_screenshots_path + screenshot + '.png'

    # скриншот, где вместо баннера расположен одноцветный прямоугольник
    path_special = raw_screenshots_path + special_screenshot + '.png'

    screenshot_normal_png = Image.open(path_normal)
    screenshot_special_png = Image.open(path_special)
    screenshot_width = screenshot_special_png.size[0]
    screenshot_height = screenshot_special_png.size[1]
    screenshot_normal_pix = screenshot_normal_png.load()
    screenshot_special_pix = screenshot_special_png.load()

    min_sum = screenshot_width + screenshot_height
    x1, y1 = 0, 0

    min_diff = screenshot_width + screenshot_height
    x2, y2 = 0, 0

    max_sum = 0
    x3, y3 = 0, 0

    max_diff = 0.0
    x4, y4 = 0, 0

    # определяем углы
    for x in range(screenshot_width):
        for y in range(screenshot_height):
            colors_normal = screenshot_normal_pix[x, y]
            colors_special = screenshot_special_pix[x, y]
            summ = x + y
            diff = x - y
            if colors_normal != colors_special:
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

    print("Vertices: (%s, %s), (%s, %s), (%s, %s), (%s, %s)" % (x1, y1, x2, y2, x3, y3, x4, y4))

    # сохраняем скриншот с вставленным баннером
    screenshot_normal_png.save(path)
    print("Save normal screenshot with %s" % path)

    # рисуем границы на изображении
    def paint_edge(ax, ay, bx, by):
        if abs(bx - ax) >= abs(by - ay):
            step_y = (by - ay) / abs(bx - ax)
            cur_y = ay
            for cur_x in range(ax, bx, np.sign(bx - ax)):
                screenshot_normal_pix[cur_x, cur_y] = special_color_rbg
                cur_y += step_y
        else:
            step_x = (bx - ax) / abs(by - ay)
            cur_x = ax
            for cur_y in range(ay, by, np.sign(by - ay)):
                screenshot_normal_pix[cur_x, cur_y] = special_color_rbg
                cur_x += step_x

    paint_edge(x1, y1, x2, y2)
    paint_edge(x2, y2, x3, y3)
    paint_edge(x3, y3, x4, y4)
    paint_edge(x4, y4, x1, y1)

    # сохраняем скриншот с нарисванными границами
    path = "boxes/%s.png" % screenshot
    screenshot_normal_png.save(path)
    print("Save boxes screenshot with %s" % path)

    file_screenshots_csv.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %
                               (screenshot, room, wall_index, image,
                                x1, y1, x2, y2, x3, y3, x4, y4))


# Скрипт для определения границ баннеров на сгенерируемых скриншотах 3d моделей
if __name__ == "__main__":
    byte_io = BytesIO()

    file_screenshots_csv = open('screenshot.csv', 'a')

    ply_data = pandas.read_csv('rawScreenshots.csv').values

    raw_screenshots_path = 'raw_screenshots/'
    result_path = 'screenshots/'

    for i in range(len(ply_data)):
        process_screenshot(ply_data[i], raw_screenshots_path, result_path)

    sys.exit()
