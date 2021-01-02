import uuid

import pandas
import numpy as np
import pyvista as pv
import sys

session_id = uuid.uuid4()

cpos = [(0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
        (0.0, 0.0, 1.0)]

file_screenshots_csv = open('screenshots.csv', 'a')

ply_data = pandas.read_csv('plyGenerated.csv').values

current_data = ply_data[1]

[main_ply,special_ply,special_color,room,wall_index,image] = current_data

print(main_ply,special_ply,special_color,room,wall_index,image)

mesh_path = "generated/%s.ply" % main_ply

mesh = pv.read(mesh_path)
[cpos2, _] = mesh.plot(cpos=cpos, screenshot=True, rgb=True)

plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(mesh, rgb=True)
plotter.camera_position = cpos2

screenshot_uuid = uuid.uuid4()

file_screenshots_csv.write("%s,%s,%s,%s\n" %
                           (screenshot_uuid, room, wall_index, image))

path = "raw_screenshots/%s.png" % screenshot_uuid
plotter.show(screenshot=path)
print("Save screenshot with path: %s" % path)

sys.exit()
