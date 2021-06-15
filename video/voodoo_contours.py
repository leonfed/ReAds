import cv2
import numpy as np

from utils.corners import sort_contour


def get_points(point_3d, frame_params):
    [X, Y, Z] = list(map(lambda t: float(t), point_3d.split("\t")))

    params = list(
        map(lambda t: float(t),
            filter(lambda t: len(t) > 0 and t != '\n',
                   frame_params.split("\t"))
            )
    )

    [Cx, Cy, Cz,
     Ax, Ay, Az,
     Hx, Hy, Hz,
     Vx, Vy, Vz,
     K3, K5, sx, sy,
     Width, Height,
     ppx, ppy, f, fov,
     H0x, H0y, H0z,
     V0x, V0y, V0z] = params

    M1 = np.array([
        [Hx, Hy, Hz],
        [Vx, Vy, Vz],
        [Ax, Ay, Az]
    ])

    M2 = np.array([
        [1., 0., 0., -Cx],
        [0., 1., 0., -Cy],
        [0., 0., 1., -Cz]
    ])

    M3 = np.array([X, Y, Z, 1.])

    res = np.dot(np.dot(M1, M2), M3)

    x_1 = res[0]
    y_1 = res[1]
    z_1 = res[2]

    x = x_1 / z_1 + 0.5 * (Width - 1)
    y = y_1 / z_1 + 0.5 * (Height - 1)

    return x, y


def expand_contours(contours_path, frames_params_path, points_3d_path, frames_size):
    first_contour = np.load(contours_path + "0.npy")
    first_contour = sort_contour(first_contour)

    with open(frames_params_path) as f:
        frames_params = f.readlines()

    with open(points_3d_path) as f:
        points_3d = f.readlines()

    selected_points_3d = []
    first_points = []

    for i in range(len(points_3d)):
        x, y = get_points(points_3d[i], frames_params[0])
        dist = cv2.pointPolygonTest(first_contour, (x, y), True)
        if dist >= -20.0:
            selected_points_3d.append(points_3d[i])
            first_points.append([x, y])

    first_points = np.array(first_points)

    for i in range(1, frames_size):
        cur_points = []

        for j in range(len(selected_points_3d)):
            x, y = get_points(selected_points_3d[j], frames_params[i])
            cur_points.append([x, y])

        cur_points = np.array(cur_points)

        h, _ = cv2.findHomography(first_points, cur_points)

        cur_contour = cv2.perspectiveTransform(np.array([first_contour], dtype=float), h)
        cur_contour = np.array(cur_contour[0], dtype=int)

        np.save(contours_path + str(i), cur_contour)


# проецирует контур первого контура на другие контуры, опирайся на выход voodoo
if __name__ == "__main__":
    contours_path = 'data/contours/'
    frames_params_path = 'data/voodoo/frames_params.tsv'
    points_3d_path = 'data/voodoo/3d_points.tsv'
    frames_size = 225
    expand_contours(contours_path, frames_params_path, points_3d_path, frames_size)
