import random
import shutil

import pandas
import json
import os
import xml.etree.ElementTree as ET

result = {}

##############################################################################
# Screenshots
##############################################################################

# ply_data = pandas.read_csv('banner/annotation.csv').values
#
# for i in range(len(ply_data)):
#     current_data = ply_data[i]
#     [screenshot, room, wall_index, image, x1, y1, x2, y2, x3, y3, x4, y4] = current_data
#
#     polygon = {"shape_attributes": {"all_points_x": [x1, x2, x3, x4, x1], "all_points_y": [y1, y2, y3, y4, y1]}}
#     current_object = {"filename": "%s.png" % screenshot, "regions": {"0": polygon}}
#
#     result[screenshot] = current_object


##############################################################################
# Real photos
##############################################################################

directory = '/home/fedleonid/Study/diploma/annotations_photos'

files = os.listdir(directory)

random.shuffle(files)

test_files = files[0:50]
train_files = files[51:]

print(test_files)
print(train_files)

for file in test_files:
    filename = file.split('.')[0]
    shutil.copy('/home/fedleonid/Study/diploma/photos/%s.jpg' % filename,
                '/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg' % filename)

for file in train_files:
    filename = file.split('.')[0]
    shutil.copy('/home/fedleonid/Study/diploma/photos/%s.jpg' % filename,
                '/home/fedleonid/Study/diploma/detectron_train_data/real/%s.jpg' % filename)

for file in train_files:
    filename = file.split('.')[0]
    print(filename)
    tree = ET.parse(directory + "/" + filename + ".xml")

    objects = tree.getroot().findall("object")

    regions = {}
    polygon_cnt = 0

    for obj in objects:
        xml_points = obj.find('polygon').findall('pt')
        points_x = []
        points_y = []
        for xp in xml_points:
            x = int(xp.find('x').text)
            y = int(xp.find('y').text)
            points_x.append(x)
            points_y.append(y)

        points_x.append(points_x[0])
        points_y.append(points_y[0])

        polygon = {"shape_attributes": {"all_points_x": points_x, "all_points_y": points_y}}
        regions[str(polygon_cnt)] = polygon

        polygon_cnt += 1

    current_object = {"filename": "%s.jpg" % filename, "regions": regions}

    result[filename] = current_object

##############################################################################
##############################################################################

file_screenshots_csv = open('/home/fedleonid/Study/diploma/detectron_train_data/real/via_region_data.json', 'w')
file_screenshots_csv.write(json.dumps(result))
