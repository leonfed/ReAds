import random
import shutil

import pandas
import json
import os
import xml.etree.ElementTree as ET

directory = '/home/fedleonid/Study/diploma/annotations_photos'

all_files = os.listdir('source')
filtered = filter(lambda x: not x.startswith('synthetic'), all_files)
files = list(map(lambda x: x.split('.')[0], filtered))
print(files)

for filename in files:
    tree = ET.parse(directory + "/" + filename + ".xml")

    object = tree.getroot().findall("object")[0]
    xml_points = object.find('polygon').findall('pt')

    left_top = (10000, 10000)
    right_top = (0, 10000)
    left_bottom = (10000, 0)
    right_bottom = (0, 0)

    for xp in xml_points:
        x = int(xp.find('x').text)
        y = int(xp.find('y').text)
        if x + y < left_top[0] + left_top[1]:
            left_top = (x, y)
        if x - y > right_top[0] - right_top[1]:
            right_top = (x, y)
        if y - x > left_bottom[1] - left_bottom[0]:
            left_bottom = (x, y)
        if x + y > right_bottom[0] + right_bottom[1]:
            right_bottom = (x, y)
    print('%s,%s,%s,%s,%s,%s,%s,%s,%s' % (filename,
                                         left_top[0], left_top[1],
                                         right_top[0], right_top[1],
                                         right_bottom[0], right_bottom[1],
                                         left_bottom[0], left_bottom[1]))
