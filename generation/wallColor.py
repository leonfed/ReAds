import sys
from random import randint

import numpy as np
from plyfile import PlyData

# Скрипт, который раскрашивает стены. Удобен для дебага
if __name__ == "__main__":

    plydata = PlyData.read('/home/fedleonid/Study/diploma/replica_v1/apartment_2/habitat/mesh_semantic.ply')
    print(plydata)
    face = plydata['face']
    vertex = plydata['vertex']
    face_data = np.array(face.data.copy())
    vertex_data = np.array(vertex.data.copy())

    print('face len: %s' % len(face.data))
    print('vertex len: %s' % len(vertex.data))
    # print(face.data)
    # print(vertex.data)

    vertex_len = len(vertex.data)

    indexes = set()

    wall_ids = {76}

    for i in range(len(face.data)):
        if wall_ids.__contains__(face.data[i][1]):
            for e in face.data[i][0]:
                indexes.add(e)

    print(len(indexes))

    points = []

    for i in indexes:
        vertex_data[i] = (vertex_data[i][0], vertex_data[i][1], vertex_data[i][2],
                          vertex_data[i][3], vertex_data[i][4], vertex_data[i][5],
                          randint(0, 255), randint(0, 255), randint(0, 255))

    vertex.data = vertex_data
    face.data = face_data

    # print(face.data)
    # print(vertex.data)

    plydata.elements = [vertex, face]

    plydata.write('mesh_semantic.ply')

    sys.exit()
