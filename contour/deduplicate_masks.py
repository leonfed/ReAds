import cv2
import numpy as np
from PIL import Image
import os


def to_rgb(mask_value):
    return (0., 0., 0.) if mask_value else (255., 255., 255.)


all_files = os.listdir('examples')
filtered = filter(lambda x: x.endswith('npy') and not x.startswith('scores'), all_files)
masks_files = list(map(lambda x: x.split('.')[0], filtered))
print(masks_files)

for filename in masks_files:
    print(filename)
    path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
    masks = np.load('examples/%s.npy' % filename)
    scores = np.load('examples/scores_%s.npy' % filename)

    original_image = cv2.imread(path)

    if len(masks) < 1:
        np.save('masks/%s' % filename, np.array([]))
        np.save('masks/scores_%s' % filename, np.array([]))
        continue

    # убрать накладывающиеся
    new_masks = [masks[0]]
    new_scores = [scores[0]]

    def is_intersection(mask1, mask2):
        count = 0
        all_count = 0
        for i in range(len(mask1)):
            for j in range(len(mask1[0])):
                if mask1[i][j]:
                    all_count += 1
                if mask2[i][j]:
                    all_count += 1
                if mask1[i][j] and mask2[i][j]:
                    count += 1
        return count > all_count / 10

    for i in range(len(masks)):
        is_added = False
        for j in range(len(new_masks)):
            if is_intersection(masks[i], new_masks[j]):
                is_added = True
                for x in range(len(new_masks[j])):
                    for y in range(len(new_masks[j][0])):
                        if masks[i][x][y]:
                            new_masks[j][x][y] = True
                new_scores[j] = (new_scores[j] + scores[i]) / 2
        if not is_added:
            new_masks.append(masks[i])
            new_scores.append(scores[i])

    np.save('masks/%s' % filename, np.array(new_masks))
    np.save('masks/scores_%s' % filename, np.array(new_scores))