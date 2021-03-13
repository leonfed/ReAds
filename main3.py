import uuid

from plyfile import PlyData
import numpy as np
from random import randint
from random import shuffle
import random
import sys
from PIL import Image

from room import get_room
from utils import rgb2hex

images_count = 98
iterations_count = 10
distance_neighbors = 0.1

room_name, wall_indexes = get_room(7)
min_plot_width = 0.5
max_plot_width = 1.2

session_id = uuid.uuid4()

path = 'mesh_semantic.ply'
plydata = PlyData.read(path)
face = plydata['face']
vertex = plydata['vertex']

vertex_len = len(vertex.data)

images_array = [i for i in range(1, images_count + 1)]
while len(images_array) < iterations_count:
    images_array = images_array.copy() + images_array.copy()
shuffle(images_array)

file_ply_generated_csv = open('plyGenerated.csv', 'a')

for iteration in range(iterations_count):
    print("Start iteration %s" % iteration)
    face_data = np.array(face.data.copy())
    vertex_data = np.array(vertex.data.copy())
    vertex_data_copy = vertex.data.copy()
    face_data_copy = face.data.copy()
    vertex_data_0_copy = vertex_data[0].copy()
    face_data_0_copy = face_data[0].copy()

    image_number = images_array[iteration]
    # image_number = 6
    path = "images/%s.jpg" % image_number
    print("Path to image: %s" % path)
    image = Image.open(path)
    image = image.rotate(180, expand=True)
    image_width = image.size[0]
    image_height = image.size[1]
    image_pix = image.load()

    all_colors = set()
    for image_x in range(image_width):
        for image_y in range(image_height):
            color = image_pix[image_x, image_y]
            all_colors.add(color)
    special_color = (-1, -1, -1)
    while special_color[0] == -1:
        special_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        if special_color in all_colors:
            special_color = (-1, -1, -1)

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
        fixed_coordinate_value = min_x - eps if randint(0, 1) == 0 else max_x + eps
    elif len_y / sum_len < percent:
        fixed_coordinate_idx = 1
        fixed_coordinate_value = min_y - eps if randint(0, 1) == 0 else max_y + eps
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

    vertex_data[0] = vertex_data_0_copy
    face_data[0] = face_data_0_copy

    isOk = True
    for i in range(5):
        idx = randint(0, len(appended_vertices) - 1)
        thisIndexIsOk = False
        for p in points:
            dx = abs(p[1] - appended_vertices[idx][0])
            dy = abs(p[2] - appended_vertices[idx][1])
            if dx < distance_neighbors and dy < distance_neighbors:
                thisIndexIsOk = True
                break
        if not thisIndexIsOk:
            isOk = False
            break
    if not isOk:
        print("Image is not at wall")
        continue

    appended_vertices_normal = np.array(appended_vertices)
    appended_vertices_special = appended_vertices_normal.copy()
    for i in range(len(appended_vertices_special)):
        v = appended_vertices_special[i]
        appended_vertices_special[i] = (v[0], v[1], v[2],
                                        v[3], v[4], v[5],
                                        special_color[0], special_color[1], special_color[2])

    face_data = np.append(face_data, appended_faces)
    face.data = face_data
    vertex_data_normal = np.append(vertex_data, appended_vertices_normal)
    vertex_data_special = np.append(vertex_data, appended_vertices_special)

    vertex.data = vertex_data_normal
    plydata.elements = [vertex, face]
    ply_normal_uuid = uuid.uuid4()
    path = 'generated/%s.ply' % ply_normal_uuid
    print("Path to generated normal ply: %s" % path)
    plydata.write(path)

    vertex.data = vertex_data_special
    plydata.elements = [vertex, face]
    ply_special_uuid = uuid.uuid4()
    path = 'generated/%s.ply' % ply_special_uuid
    print("Path to special normal ply: %s" % path)
    plydata.write(path)

    file_ply_generated_csv.write("%s,%s,%s,%s,%s,%s\n" %
                                 (ply_normal_uuid, ply_special_uuid,
                                  rgb2hex(special_color), room_name, wall_index, image_number))

    vertex.data = vertex_data_copy
    face.data = face_data_copy
    plydata.elements = [vertex, face]

sys.exit()
