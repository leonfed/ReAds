import uuid

import numpy as np
import pyvista as pv
import sys

cpos = [(0.0, 0.0, 0.0),
        (1.0, 1.0, 1.0),
        (0.0, 0.0, 1.0)]

mesh = pv.read("mesh_semantic.ply")
[cpos2, _] = mesh.plot(cpos=cpos, screenshot=True, rgb=True)

sys.exit()
