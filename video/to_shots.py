import os
import shutil

import cv2

# удалить содержимое папки
shutil.rmtree('data/input')
os.makedirs('data/input')

video_obj = cv2.VideoCapture('data/original.mp4')
count = 0

success, image = video_obj.read()

while success:
    print(count)
    cv2.imwrite("data/input/%s.jpg" % count, image)
    count += 1
    success, image = video_obj.read()
