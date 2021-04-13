import shutil

import cv2
import numpy as np
import pandas
from PIL import Image
import os
import xml.etree.ElementTree as ET


def to_rgb(mask_value):
    return (0., 0., 0.) if mask_value else (255., 255., 255.)


contours_files = os.listdir('../test_data/quad_output')
contours_files = sorted(contours_files)
print(contours_files)
print('\n')

synthetic_gt_data = pandas.read_csv('../test_data/input/synthetic_ground_truth.csv').values
# filename,x1,y1,x2,y2,x3,y3,x4,y4
synthetic_gt_contours = {}
for d in synthetic_gt_data:
    filename, x1, y1, x2, y2, x3, y3, x4, y4 = d
    c = np.array([[x1, y1], [x2, y2], [x4, y4], [x4, y4]])
    synthetic_gt_contours[filename] = c

for raw_filename in contours_files:
    filename = raw_filename.split('.')[0]

    mask = np.load('../test_data/masks/%s.npy' % filename)

    contour = np.load('../test_data/quad_output/' + raw_filename)
    contour = np.append(contour, [contour[0]], axis=0)
    contour = np.vectorize(lambda x: int(x))(contour)


    def get_real_gt_contour():
        tree = ET.parse('/home/fedleonid/Study/diploma/annotations_photos/' + filename + ".xml")
        objects = tree.getroot().findall("object")
        gt_contour = []

        for obj in objects:
            xml_points = obj.find('polygon').findall('pt')
            points = []
            for xp in xml_points:
                x = int(xp.find('x').text)
                y = int(xp.find('y').text)
                points.append([x, y])
            points.append(points[0])
            points = np.array(points)

            # Проверяем пересекается ли этот контур с найденным
            is_intersection = False
            for p in contour:
                dist = cv2.pointPolygonTest(points, (p[0], p[1]), False)
                is_intersection = is_intersection or dist >= 0.0
            for p in points:
                dist = cv2.pointPolygonTest(contour, (p[0], p[1]), False)
                is_intersection = is_intersection or dist >= 0.0

            if is_intersection:
                gt_contour = points
                break

        if len(gt_contour) == 0:
            return None

        return gt_contour


    def get_synthetic_gt_contour():
        if synthetic_gt_contours.__contains__(filename):
            return synthetic_gt_contours[filename]
        else:
            return None


    gt_contour = get_synthetic_gt_contour() if filename.startswith('synthetic_') else get_real_gt_contour()

    if gt_contour is None:
        print("%s\t%s\t%s\t%s\t%s" % (raw_filename, '-', '-', '-', '-'))
        continue

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for i in range(len(mask)):
        for j in range(len(mask[0])):
            point = (j, i)
            is_in_contour = cv2.pointPolygonTest(contour, point, False) >= 0.0
            is_in_gt = cv2.pointPolygonTest(gt_contour, point, False) >= 0.0
            if is_in_contour and is_in_gt:
                tp += 1
            elif is_in_contour and is_in_gt:
                fp += 1
            elif not is_in_contour and is_in_gt:
                fn += 1
            elif not is_in_contour and not is_in_gt:
                tn += 1

    print("%s\t%s\t%s\t%s\t%s" % (raw_filename, tp, tn, fp, fn))
