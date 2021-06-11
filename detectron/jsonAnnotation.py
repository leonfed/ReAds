import json
import os
import xml.etree.ElementTree as ET

import pandas

# Строит json аннотацию датасеты, нужную для обучения MASK R-CNN (detectron)
if __name__ == "__main__":
    dataset_path = 'detectron_train_data'

    files = os.listdir(dataset_path)

    # отделяем реальные фото от синтететических
    real_files = list(filter(lambda x: not x.startswith('synthetic_'), files))
    synthetic_data = pandas.read_csv('detectron_train_data/synthetic_ground_truth.csv').values

    result = {}

    # обрабатываем синтетические фото
    for i in range(len(synthetic_data)):
        current_data = synthetic_data[i]
        [filename, x1, y1, x2, y2, x3, y3, x4, y4] = current_data
        polygon = {"shape_attributes": {"all_points_x": [x1, x2, x3, x4, x1], "all_points_y": [y1, y2, y3, y4, y1]}}
        current_object = {"filename": "%s.png" % filename, "regions": {"0": polygon}}

        result[filename] = current_object

    print("Synthetic - OK")

    # обрабатываем реальные фото
    for file in real_files:
        filename = file.split('.')[0]
        tree = ET.parse('annotations_photos/' + filename + ".xml")

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

    print("Real - OK")

    file_screenshots_csv = open('detectron_train_data/via_region_data.json', 'w')
    file_screenshots_csv.write(json.dumps(result))

    print("OK")
