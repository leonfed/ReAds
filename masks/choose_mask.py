import os
import shutil

import cv2
import numpy as np


def to_rgb(mask_value):
    return (0., 0., 0.) if mask_value else (255., 255., 255.)


# удалить содержимое папки
shutil.rmtree('../test_data/masks')
os.makedirs('../test_data/masks')

all_files = os.listdir('../test_data/mask_rcnn_output')
filtered = filter(lambda x: x.endswith('npy') and not x.startswith('scores'), all_files)
masks_files = list(map(lambda x: x.split('.')[0], filtered))
print(masks_files)

for filename in masks_files:
    print(filename)
    masks = np.load('../test_data/mask_rcnn_output/%s.npy' % filename)
    scores = np.load('../test_data/mask_rcnn_output/scores_%s.npy' % filename)

    if len(masks) < 1:
        print("Skip " + filename + " because masks is empty")
        continue

    input_filename = filename + '.png' if filename.startswith('synthetic_') else filename + '.jpg'
    original_image = cv2.imread('../test_data/input/' + input_filename)

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


    for i in range(1, len(masks)):
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

    masks = new_masks
    scores = new_scores

    # выбираем лучшую маску из всех по score
    best_mask_index = 0
    best_mask_score = scores[0]
    for i in range(1, len(masks)):
        if scores[i] > best_mask_score:
            best_mask_score = scores[i]
            best_mask_index = i

    if best_mask_score < 0.85:
        print("Skip because score is " + str(best_mask_score))
    else:
        np.save('../test_data/masks/%s' % filename, np.array(masks[best_mask_index]))
