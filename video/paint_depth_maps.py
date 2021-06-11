import os
import numpy as np
import matplotlib.pyplot as plt

# рисует карты глубины
if __name__ == "__main__":
    files = os.listdir('data/depth_maps')
    print(len(files))

    for filename in files:
        print(filename)
        data = np.load('data/depth_maps/' + filename)
        name_for_save = filename.split('.')[0]
        plt.imshow(data)
        plt.savefig('data/depth_maps_images/' + name_for_save)
        plt.close()
