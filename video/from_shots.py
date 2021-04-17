import cv2
import os
from PIL import Image

files_count = len(os.listdir('data/final_result'))
print(files_count)

fps = 24

image = Image.open('data/final_result/1.jpg')
frame_width = image.size[0]
frame_height = image.size[1]

out = cv2.VideoWriter('data/from_shots.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), fps,
                      (frame_width, frame_height))

for i in range(files_count):
    print(i)
    path = 'data/final_result/%s.jpg' % i
    frame = cv2.imread(path)
    out.write(frame)

out.release()
