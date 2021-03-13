import uuid

import numpy as np
import pyvista as pv
import sys

cpos = [(9.284708146525697, 10.999016587210969, 10.158290748072938),
        (-0.7161442637443542, 0.998164176940918, 0.15743833780288696),
        (0.0, 0.0, 1.0)]

# mesh = pv.read("mesh_semantic.ply")
mesh = pv.read("/home/fedleonid/Study/diploma/replica_v1/room_2/habitat/mesh_semantic.ply")
# mesh = pv.read("/home/fedleonid/Study/diploma/Toronto_3D/L002.ply")
# mesh = pv.read("generated/56eba8d0-c478-45e8-b59a-59bc14c20f8c.ply")

[cpos2, _] = mesh.plot(cpos=cpos, screenshot=True, rgb=True)

print(cpos2)

sys.exit()
