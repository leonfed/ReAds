import cv2
import os

files_count = len(os.listdir('data/test_shots'))
print(files_count)

frame_width = 1280
frame_height = 720

out = cv2.VideoWriter('test_from_shots.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))

for i in range(files_count):
    print(i)
    path = 'data/test_shots/%s.jpg' % i
    frame = cv2.imread(path)
    out.write(frame)

out.release()

