import cv2
import numpy as np


# считает метрику, показывающую, насколько большую площадь пересечения имеет маска и контур
def calc_score(mask_path, contour_path):
    mask = np.load(mask_path)
    contour = np.load(contour_path)

    score = 0

    for i in range(0, len(mask)):
        for j in range(0, len(mask[0])):
            dist = cv2.pointPolygonTest(contour, (j, i), True)
            if mask[i][j] and dist >= 0.0:
                score += 1
            if not mask[i][j] and dist >= 0.0:
                score -= 1

    return score
