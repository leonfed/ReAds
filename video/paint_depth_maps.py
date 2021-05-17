import os
import numpy as np
import matplotlib.pyplot as plt

# рисует карты глубины
if __name__ == "__main__":
    files = os.listdir('data_4/depth_maps')
    print(len(files))

    for filename in files:
        print(filename)
        data = np.load('data_4/depth_maps/' + filename)
        name_for_save = filename.split('.')[0]
        plt.imshow(data)
        plt.savefig('data_4/depth_maps_images/' + name_for_save)
        plt.close()
