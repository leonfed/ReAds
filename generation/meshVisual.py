import sys

import pyvista as pv

# Скрипт для визуализации 3d модели с помощью pyvista
if __name__ == "__main__":
    # расположение камеры
    cpos = [(9.284708146525697, 10.999016587210969, 10.158290748072938),
            (-0.7161442637443542, 0.998164176940918, 0.15743833780288696),
            (0.0, 0.0, 1.0)]

    mesh = pv.read("generated/56eba8d0-c478-45e8-b59a-59bc14c20f8c.ply")

    [cpos2, _] = mesh.plot(cpos=cpos, screenshot=True, rgb=True)

    # выводим координаты камеры во время выхода из режима наблюдения
    print(cpos2)

    sys.exit()
