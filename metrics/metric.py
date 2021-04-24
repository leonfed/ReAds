import os
import xml.etree.ElementTree as ET
import cv2
import numpy as np
import pandas


# получить ground-truth контур для реального изображения
def get_real_gt_contour(real_gt_path, contour):
    tree = ET.parse(real_gt_path + filename + ".xml")
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


# получить ground-truth контур для синтетического изображения
def get_synthetic_gt_contour(synthetic_gt_contours):
    if synthetic_gt_contours.__contains__(filename):
        return synthetic_gt_contours[filename]
    else:
        return None


# посчитать метрику для одного изображения
def process(image_name, dir_path, real_gt_path, masks_path, contours_files, synthetic_gt_contours):
    filename = image_name.split('.')[0]

    if not contours_files.__contains__(filename):
        print("%s\t%s\t%s\t%s\t%s" % (image_name, '-', '-', '-', '-'))
        return

    mask = np.load(masks_path + filename + '.npy')

    contour = np.load(dir_path + filename + '.npy')
    contour = np.append(contour, [contour[0]], axis=0)
    contour = np.vectorize(lambda x: int(x))(contour)

    gt_contour = get_synthetic_gt_contour(synthetic_gt_contours) \
        if filename.startswith('synthetic_') \
        else get_real_gt_contour(real_gt_path, contour)

    if gt_contour is None:
        print("%s\t%s\t%s\t%s\t%s" % (raw_image_name, '-', '-', '-', '-'))
        return

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
            elif is_in_contour and not is_in_gt:
                fp += 1
            elif not is_in_contour and is_in_gt:
                fn += 1
            elif not is_in_contour and not is_in_gt:
                tn += 1

    print("%s\t%s\t%s\t%s\t%s" % (raw_image_name, tp, tn, fp, fn))


# Посчитать метрики для контуров. Выводит посчитанные метрики в консоль
if __name__ == "__main__":
    # путь до контуров, которые посчитал алгоритм
    dir_path = '../test_data/edge_output/'

    # путь до ground-truth контуров синтетических изображений
    synthetic_gt_path = '../test_data/input/synthetic_ground_truth.csv'

    # путь до ground-truth контуров реальных изображений
    real_gt_path = '/home/fedleonid/Study/diploma/annotations_photos/'

    # путь до ground-truth контуров реальных изображений
    images_path = '../test_data/input/'

    # путь до масок баннеров
    masks_path = '../test_data/masks/'

    all_images = os.listdir(images_path)
    all_images = sorted(all_images)

    contours_files = os.listdir(dir_path)
    contours_files = set(map(lambda x: x.split('.')[0], contours_files))
    print(contours_files)
    print('\n')

    synthetic_gt_data = pandas.read_csv(synthetic_gt_path).values
    synthetic_gt_contours = {}
    for d in synthetic_gt_data:
        filename, x1, y1, x2, y2, x3, y3, x4, y4 = d
        c = np.array([[x1, y1], [x2, y2], [x4, y4], [x4, y4]])
        synthetic_gt_contours[filename] = c

    for raw_image_name in all_images:
        process(raw_image_name, dir_path, real_gt_path, masks_path, contours_files, synthetic_gt_contours)
