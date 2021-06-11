import os
import random
import shutil

import pandas

# Вспомогающий файл для формирования датасетов (для обучения и для тренировки)
if __name__ == "__main__":
    # прочитать синтетические фото
    synthetic_data = pandas.read_csv('../generation/banner/annotation.csv').values
    synthetic_data = [t.copy() for t in synthetic_data]
    random.shuffle(synthetic_data)

    # разделить на тестовыей и тренировычный
    to_test_data_count = 30
    test_synthetic_data = synthetic_data[:to_test_data_count]
    train_synthetic_data = synthetic_data[to_test_data_count:]

    synthetic_index = 0

    # файлы для запоминания того, где располежены углы баннеров
    test_synthetic_csv = open('detectron_test_data/synthetic_ground_truth.csv', 'w')
    test_synthetic_csv.write("filename,x1,y1,x2,y2,x3,y3,x4,y4\n")
    train_synthetic_csv = open('detectron_train_data/synthetic_ground_truth.csv', 'w')
    train_synthetic_csv.write("filename,x1,y1,x2,y2,x3,y3,x4,y4\n")

    # скопировать датасеты
    for current_data in test_synthetic_data:
        [screenshot, room, wall_index, image, x1, y1, x2, y2, x3, y3, x4, y4] = current_data
        filename = 'synthetic_' + str(synthetic_index)
        synthetic_index += 1
        shutil.copy('../generation/banner/%s.png' % screenshot, 'detectron_test_data/%s.png' % filename)
        test_synthetic_csv.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (filename, x1, y1, x2, y2, x3, y3, x4, y4))
    for current_data in train_synthetic_data:
        [screenshot, room, wall_index, image, x1, y1, x2, y2, x3, y3, x4, y4] = current_data
        filename = 'synthetic_' + str(synthetic_index)
        synthetic_index += 1
        shutil.copy('../generation/banner/%s.png' % screenshot, 'detectron_train_data/%s.png' % filename)
        train_synthetic_csv.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (filename, x1, y1, x2, y2, x3, y3, x4, y4))

    print("Synthetic - OK")

    # прочитать реальные фото
    annotations_files = os.listdir('annotations_photos')
    random.shuffle(annotations_files)

    # указать те, которые точно нужно поместить в тестовый датасет
    prefixes_for_test = ['951', '952', '953', '954', '957']
    test_real_data = list(filter(lambda x: prefixes_for_test.__contains__(x.split('.')[0]), annotations_files))
    annotations_files = list(filter(lambda x: not prefixes_for_test.__contains__(x.split('.')[0]), annotations_files))

    # указать сколько файлов еще закинуть в тестовый датасет
    to_test_data_count = 65
    test_real_data = test_real_data + annotations_files[:to_test_data_count]
    train_real_data = annotations_files[to_test_data_count:]

    for file in test_real_data:
        filename = file.split('.')[0]
        shutil.copy('photos/%s.jpg' % filename, 'detectron_test_data/%s.jpg' % filename)

    for file in train_real_data:
        filename = file.split('.')[0]
        shutil.copy('photos/%s.jpg' % filename, 'detectron_train_data/%s.jpg' % filename)

    print("Real - OK")
