from plyfile import PlyData
import numpy as np
from random import randint
import sys

from generation.room import get_room

room_name, wall_indexes = get_room(7)

path = '/home/fedleonid/Study/diploma/replica_v1/%s/habitat/mesh_semantic.ply' % room_name
plydata = PlyData.read(path)
face = plydata['face']
vertex = plydata['vertex']

wall_index = wall_indexes[randint(0, len(wall_indexes) - 1)]
# wall_index = 13
print("Wall index: %s" % wall_index)

vertex_indexes = set()
points = []
for i in range(len(face.data)):
    if face.data[i][1] == wall_index:
        for e in face.data[i][0]:
            vertex_indexes.add(e)
for i in vertex_indexes:
    points.append((i, vertex.data[i][0], vertex.data[i][1], vertex.data[i][2]))

points_x = [p[1] for p in points]
points_y = [p[2] for p in points]
points_z = [p[3] for p in points]
min_x = min(points_x)
max_x = max(points_x)
len_x = max_x - min_x
print("X. Min: %s Max: %s Len: %s" % (min_x, max_x, len_x))
min_y = min(points_y)
max_y = max(points_y)
len_y = max_y - min_y
print("Y. Min: %s Max: %s Len: %s" % (min_y, max_y, len_y))

if len_x > len_y:
    sin_angle = len_y / len_x
elif len_x < len_y:
    sin_angle = len_x / len_y
else:
    print("What the hell!! len_x == len_y")
    sys.exit()

angle = np.arcsin(sin_angle)
# angle = 0.64
print("Angle: %s" % angle)

for i in range(len(vertex.data)):
    x = vertex.data[i][0]
    y = vertex.data[i][1]
    new_x = x * np.cos(angle) - y * np.sin(angle)
    new_y = x * np.sin(angle) + y * np.cos(angle)
    vertex.data[i] = (new_x, new_y, vertex.data[i][2],
                      vertex.data[i][3], vertex.data[i][4], vertex.data[i][5],
                      vertex.data[i][6], vertex.data[i][7], vertex.data[i][8])

path = 'mesh_semantic.ply'
plydata.write(path)

sys.exit()
