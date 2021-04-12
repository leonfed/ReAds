import cv2

video_obj = cv2.VideoCapture('data/test.mp4')
count = 0

success, image = video_obj.read()

while success:
    cv2.imwrite("data/test_shots/%s.jpg" % count, image)
    count += 1
    success, image = video_obj.read()
