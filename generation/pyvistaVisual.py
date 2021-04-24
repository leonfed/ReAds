import uuid

import pandas
import numpy as np
import pyvista as pv
import sys

# Скрипт для ручного производства скриншотов
if __name__ == "__main__":
    session_id = uuid.uuid4()

    # координаты камеры
    cpos_0 = [(19.20555104420307, 13.761262075163152, 16.523463503576544),
              (2.5814136266708374, -2.8628753423690796, -0.10067391395568848),
              (0.0, 0.0, 1.0)]

    # файл для того, чтобы записывать получившиеся скриншоты
    file_screenshots_csv = open('rawScreenshots.csv', 'a')

    # чтение генерируемых 3d моделей
    ply_data = pandas.read_csv('plyGenerated.csv').values

    # выбираем одну модель
    current_data = ply_data[0]

    [main_ply, special_ply, special_color, room, wall_index, image] = current_data

    print(main_ply, special_ply, special_color, room, wall_index, image)

    # читаем две 3d момдели
    # mesh_normal_path - модель с вставленным баннером
    # mesh_special_path - модель, где вместо баннера расположен одноцветный прямоугольник
    mesh_normal_path = "generated/%s.ply" % main_ply
    mesh_special_path = "generated/%s.ply" % special_ply

    mesh_normal = pv.read(mesh_normal_path)
    mesh_special = pv.read(mesh_special_path)

    [custom_cpos, _] = mesh_normal.plot(cpos=cpos_0, screenshot=True, rgb=True)
    if cpos_0 == custom_cpos:
        print("Screenshot is not saved")
        sys.exit()

    screenshot_normal_uuid = uuid.uuid4()
    screenshot_special_uuid = uuid.uuid4()

    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh_normal, rgb=True)
    plotter.camera_position = custom_cpos
    path = "raw_screenshots/%s.png" % screenshot_normal_uuid
    plotter.show(screenshot=path)
    print("Save normal screenshot with path: %s" % path)

    plotter = pv.Plotter(off_screen=True)
    plotter.add_mesh(mesh_special, rgb=True)
    plotter.camera_position = custom_cpos
    path = "raw_screenshots/%s.png" % screenshot_special_uuid
    plotter.show(screenshot=path)
    print("Save special screenshot with path: %s" % path)

    file_screenshots_csv.write("%s,%s,%s,%s,%s,%s\n" %
                               (screenshot_normal_uuid, screenshot_special_uuid,
                                special_color, room, wall_index, image))

    sys.exit()
