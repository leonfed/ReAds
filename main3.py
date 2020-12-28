import uuid

from plyfile import PlyData
import numpy as np
from random import randint
import random
import sys
from PIL import Image

from room import get_room

room_name, wall_indexes = get_room(3)
min_plot_width = 0.5
max_plot_width = 1.2

session_id = uuid.uuid4()

path = '/home/fedleonid/Study/diploma/replica_v1/%s/habitat/mesh_semantic.ply' % room_name
plydata = PlyData.read(path)
face = plydata['face']
vertex = plydata['vertex']

vertex_len = len(vertex.data)

for iteration in range(3):
    print("Start iteration %s" % iteration)
    face_data = np.array(face.data.copy())
    vertex_data = np.array(vertex.data.copy())
    vertex_data_copy = vertex.data.copy()
    face_data_copy = face.data.copy()
    vertex_data_0_copy = vertex_data[0].copy()
    face_data_0_copy = face_data[0].copy()

    image_number = randint(1, 10)
    # image_number = 6
    path = "images/%s.jpg" % image_number
    print("Path to image: %s" % path)
    image = Image.open(path)
    image = image.rotate(180, expand=True)
    image_width = image.size[0]
    image_height = image.size[1]
    image_pix = image.load()

    wall_index = wall_indexes[randint(0, len(wall_indexes) - 1)]
    # wall_index = 76
    print("Wall index: %s" % wall_index)

    vertex_indexes = set()
    points = []
    for i in range(len(face.data)):
        if face.data[i][1] == wall_index:
            for e in face.data[i][0]:
                vertex_indexes.add(e)
    for i in vertex_indexes:
        points.append((i, vertex_data[i][0], vertex_data[i][1], vertex_data[i][2]))

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
    min_z = min(points_z)
    max_z = max(points_z)
    len_z = max_z - min_z
    print("Z. Min: %s Max: %s Len: %s" % (min_z, max_z, len_z))

    sum_len = len_x + len_y + len_z
    percent = 0.1
    eps = 0.0000001
    fixed_coordinate_idx = -1
    fixed_coordinate_value = 0.0
    if len_x / sum_len < percent:
        fixed_coordinate_idx = 0
        fixed_coordinate_value = min_x - eps if abs(min_x) < abs(max_x) else max_x + eps
    elif len_y / sum_len < percent:
        fixed_coordinate_idx = 1
        fixed_coordinate_value = min_y - eps if abs(min_y) < abs(max_y) else max_y + eps
    else:
        print("Has not chosen coordinate")
        continue
    print("Fixed coordinate: %s Value: %s" % (fixed_coordinate_idx, fixed_coordinate_value))

    plot_width = random.uniform(min_plot_width, max_plot_width)
    plot_height = plot_width * float(image_height) / float(image_width)
    print("Plot properties: %s x %s" % (plot_width, plot_height))

    step_width = plot_width / image_width
    step_height = plot_height / image_height

    if plot_height > len_z:
        print("Height is too big")
        continue
    z_start = random.uniform(min_z, max_z - plot_height)
    t_start = 0.0
    if fixed_coordinate_idx == 1:
        if plot_width > len_x:
            print("Width is too big. Length only: %s" % len_x)
            continue
        t_start = random.uniform(min_x, max_x - plot_width)
    elif fixed_coordinate_idx == 0:
        if plot_width > len_y:
            print("Width is too big. Length only: %s" % len_y)
            continue
        t_start = random.uniform(min_y, max_y - plot_width)
    else:
        print("Error")
        continue

    step_z = step_height
    step_x = 0.0
    step_y = 0.0
    x = 0.0
    y = 0.0

    if fixed_coordinate_idx == 0:
        x = t_start
        step_x = step_width
        y = fixed_coordinate_value
    elif fixed_coordinate_idx == 1:
        y = t_start
        step_y = step_width
        x = fixed_coordinate_value
    else:
        print("Error")
        continue
    print("Steps: %s, %s, %s" % (step_x, step_y, step_z))
    print("Start point: %s, %s, %s" % (x, y, z_start))

    appended_vertices = []
    appended_faces = []
    for image_x in range(image_width):
        z = z_start
        for image_y in range(image_height):
            colors = image_pix[image_x, image_y]
            vertex_data[0] = (y, x, z,
                              0.0, 0.0, 0.0,
                              colors[0], colors[1], colors[2])
            appended_vertices.append(vertex_data[0].copy())
            if image_x != image_width - 1 and image_y != image_height - 1:
                left_top = vertex_len + image_y + image_x * image_height
                left_bottom = left_top + image_height
                right_top = left_top + 1
                right_bottom = left_bottom + 1
                face_data[0] = (np.array([left_top, right_top, right_bottom, left_bottom]), 15000)
                appended_faces.append(face_data[0].copy())
            z += step_z
        x += step_x
        y += step_y

    vertex_data = np.append(vertex_data, appended_vertices)
    face_data = np.append(face_data, appended_faces)

    vertex_data[0] = vertex_data_0_copy
    face_data[0] = face_data_0_copy
    vertex.data = vertex_data
    face.data = face_data
    plydata.elements = [vertex, face]
    path = 'generated/%s__%s__%s__%s.ply' % (room_name, image_number, iteration, session_id)
    print("Path to generated ply: %s" % path)
    plydata.write(path)

    vertex.data = vertex_data_copy
    face.data = face_data_copy
    plydata.elements = [vertex, face]

sys.exit()
