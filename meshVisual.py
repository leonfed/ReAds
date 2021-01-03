import uuid

import numpy as np
import pyvista as pv
import sys

cpos = [(9.284708146525697, 10.999016587210969, 10.158290748072938),
        (-0.7161442637443542, 0.998164176940918, 0.15743833780288696),
        (0.0, 0.0, 1.0)]

# mesh = pv.read("mesh_semantic.ply")
mesh = pv.read("generated/5ec67497-1f5f-4743-80cc-c158bda15df8.ply")

[cpos2, _] = mesh.plot(cpos=cpos, screenshot=True, rgb=True)

print(cpos2)

sys.exit()
