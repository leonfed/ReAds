from plyfile import PlyData
import numpy as np
import sys
from PIL import Image

plydata = PlyData.read('/home/fedleonid/Study/diploma/replica_v1/apartment_2/habitat/mesh_semantic.ply')
print(plydata)
face = plydata['face']
vertex = plydata['vertex']
face_data = np.array(face.data.copy())
vertex_data = np.array(vertex.data.copy())

vertex_len = len(vertex.data)

image = Image.open("images/2.jpg")
image_width = image.size[0]
image_height = image.size[1]
image_pix = image.load()

min_x = 0.0
max_x = 1.0
step_x = (max_x - min_x) / image_width
min_z = -0.5
max_z = 1.0
step_z = (max_z - min_z) / image_height

fixed_y = 0.0

vertex_data_0_copy = vertex_data[0].copy()
face_data_0_copy = face_data[0].copy()

x = min_x

appended_vertices = []

for image_x in range(image_width):
    z = min_z
    for image_y in range(image_height):
        colors = image_pix[image_x, image_y]
        vertex_data[0] = (x, fixed_y, z,
                          0.0, 0.0, 0.0,
                          colors[0], colors[1], colors[2])
        appended_vertices.append(vertex_data[0].copy())
        z += step_z
    x += step_x

vertex_data = np.append(vertex_data, appended_vertices)

appended_faces = []

for image_x in range(image_width - 1):
    for image_y in range(image_height - 1):
        left_top = vertex_len + image_y + image_x * image_height
        left_bottom = left_top + image_height
        right_top = left_top + 1
        right_bottom = left_bottom + 1
        face_data[0] = (np.array([left_top, right_top, right_bottom, left_bottom]), 15000)
        appended_faces.append(face_data[0].copy())

face_data = np.append(face_data, appended_faces)

vertex_data[0] = vertex_data_0_copy
face_data[0] = face_data_0_copy

vertex.data = vertex_data
face.data = face_data

plydata.elements = [vertex, face]

plydata.write('mesh_semantic.ply')

sys.exit()
