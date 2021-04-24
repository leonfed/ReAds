import cv2

# Разбить видео на кадры
if __name__ == "__main__":
    video_obj = cv2.VideoCapture('data/original.mp4')
    count = 0

    success, image = video_obj.read()

    while True:
        print(count)
        cv2.imwrite("data/input/%s.jpg" % count, image)
        count += 1
        _, image = video_obj.read()
