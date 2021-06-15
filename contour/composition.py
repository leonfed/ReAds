import numpy as np

from contour.contour_by_color import color_find
from contour.edge_detector import edge_find
from contour.quadrilateral_contour import quad_find
from utils.score import calc_score


def compostion_find(image_path, mask_path):
    # ищем контур методом вписывания в четыреухугольник
    quad_contour_path = "tmp_quad.npy"
    quad_ok = quad_find(mask_path, quad_contour_path)
    quad_score = -np.Inf
    if quad_ok:
        quad_score = calc_score(mask_path, quad_contour_path)

    # ищем контур методом, использующим сходство цветов
    color_contour_path = "tmp_color.npy"
    color_ok = color_find(image_path, mask_path, color_contour_path)
    color_score = -np.Inf
    if color_ok:
        color_score = calc_score(mask_path, color_contour_path)

    # ищем контур методом, использующим границы объектов
    edge_contour_path = "tmp_edge.npy"
    edge_find(image_path, mask_path, edge_contour_path)
    edge_score = calc_score(mask_path, edge_contour_path)

    # выбираем лучший контур
    best_contour_path = edge_contour_path
    best_score = edge_score

    if color_score > best_score:
        best_contour_path = color_contour_path
        best_score = color_score
    if quad_score > best_score:
        best_contour_path = quad_contour_path

    return best_contour_path
