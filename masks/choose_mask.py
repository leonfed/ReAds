import os
import numpy as np


# выбрать маску для одного файла
def choose(masks_path, scores_path, result_path):
    print(filename)
    masks = np.load(masks_path)
    scores = np.load(scores_path)

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
        return False
    else:
        np.save(result_path, np.array(masks[best_mask_index]))
        return True


# Выбрать по одной маске на изображениях
if __name__ == "__main__":

    input_path = '../video/data/mask_rcnn_output/'

    # путь, куда записать результат
    result_path = '../video/data/masks/'

    all_files = os.listdir('../video/data/mask_rcnn_output')
    filtered = filter(lambda x: x.endswith('npy') and not x.startswith('scores'), all_files)
    files = list(map(lambda x: x.split('.')[0], filtered))
    print(files)

    for filename in files:
        choose(input_path + filename + '.npy', input_path + 'scores_' + filename + '.npy', result_path + filename)
