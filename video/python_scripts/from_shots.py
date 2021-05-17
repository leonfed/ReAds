import cv2
import os
from PIL import Image

# Собрать кадры в видео
if __name__ == "__main__":
    files = os.listdir('../data_4/processed_images')
    files = list(map(lambda x: x.split('.')[0], files))
    files = list(map(lambda x: int(x), files))
    min_index = min(files)
    max_index = max(files)
    print(min_index, max_index)

    fps = 24

    image = Image.open('../data_4/processed_images/%s.jpg' % files[0])
    frame_width = image.size[0]
    frame_height = image.size[1]

    out = cv2.VideoWriter('../data_4/final.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
                          (frame_width, frame_height))

    for i in range(min_index, max_index + 1):
        print(i)
        path = '../data_4/processed_images/%s.jpg' % i
        frame = cv2.imread(path)
        out.write(frame)

    out.release()
