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

masks_files = [masks_files[2]]
# masks_files = [masks_files[4]]

for filename in masks_files:
    print(filename)
    path = "/home/fedleonid/Study/diploma/detectron_test_data/input/%s.jpg" % filename
    masks = np.load('examples/%s.npy' % filename)
    scores = np.load('examples/scores_%s.npy' % filename)

    original_image = cv2.imread(path)

    if len(masks) < 1:
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

    masks = new_masks
    scores = new_scores

    # выделить контуры
    for i in range(len(masks)):
        # убираем то, в чем плохо уверены
        if scores[i] < 0.9:
            continue

        matrix = masks[i]
        black_white_image = np.array([[to_rgb(c) for c in r] for r in matrix])
        im = Image.fromarray(np.uint8(black_white_image))
        im.save('tmp.jpg')

        tmp_image = cv2.imread('tmp.jpg')
        im_bw = cv2.cvtColor(tmp_image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(im_bw, (5, 5), 0)
        im_bw = cv2.Canny(blur, 10, 90)
        contours, _ = cv2.findContours(im_bw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # аппроксимируем четырехугольником
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) > 0:
                cv2.drawContours(original_image, [approx], -1, (0, 255, 0), 3)
                cv2.drawContours(tmp_image, [approx], -1, (0, 255, 0), 3)

        cv2.imwrite('contours.jpg', tmp_image)
        exit()
    cv2.imwrite('results/%s.jpg' % filename, original_image)
