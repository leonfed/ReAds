import sys

import matplotlib.pyplot as plt
import numpy as np
import open3d as o3d

# Скрипт для визуализации 3d модели с помощью open3d
if __name__ == "__main__":
    ply_file = "mesh_semantic.etc.ply"

    pcd = o3d.io.read_point_cloud(ply_file)

    eps = 1.0

    # устанавливаем координаты наблюдателя
    zoom = 0.3
    front = [1.0, 0.001, 0.001]
    lookat = [1.0, 0.001, 0.001]
    up = [-1.0, 0.1, 0.1]

    vis = o3d.visualization.Visualizer()
    vis.create_window(visible=False)
    vis.add_geometry(pcd)
    vis.update_renderer()

    # http://www.open3d.org/docs/release/python_api/open3d.visualization.ViewControl.html?highlight=change_field_of_view
    ctr = vis.get_view_control()
    ctr.set_zoom(zoom)
    ctr.set_front(front)
    ctr.set_lookat(lookat)
    ctr.set_up(up)
    img = vis.capture_screen_float_buffer(True)

    fig = plt.imshow(np.asarray(img))
    plt.box(False)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)
    plt.show()

    o3d.visualization.draw_geometries([pcd],
                                      zoom=zoom,
                                      front=front,
                                      lookat=lookat,
                                      up=up,
                                      mesh_show_back_face=False)

    sys.exit()
