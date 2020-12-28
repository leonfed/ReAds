import uuid

import numpy as np
import pyvista as pv
import sys

session_id = uuid.uuid4()

cpos = [(0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
        (0.0, 0.0, 1.0)]

# mesh = pv.read("mesh_semantic.ply")
mesh = pv.read("generated/apartment_1__10__2__70b60121-1b57-4486-97fb-33dc5f1912f9.ply")
[cpos2, _] = mesh.plot(cpos=cpos, screenshot=True, rgb=True)

plotter = pv.Plotter(off_screen=True)
plotter.add_mesh(mesh, rgb=True)
plotter.camera_position = cpos2
path = "raw_screenshots/%s.png" % session_id
plotter.show(screenshot=path)
print("Save screenshot with path: %s" % path)

sys.exit()
