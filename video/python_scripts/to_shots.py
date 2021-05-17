import cv2


def get_name_for_voodoo(idx):
    name = '0' * 3 + str(idx)
    return name[-3:]


# Разбить видео на кадры
if __name__ == "__main__":
    video_obj = cv2.VideoCapture('../data_4/original.mp4')
    count = 0

    success, image = video_obj.read()

    while success:
        print(count)
        cv2.imwrite("../data_4/input/%s.jpg" % count, image)
        cv2.imwrite("../data_4/for_voodoo/%s.jpg" % get_name_for_voodoo(count), image)
        count += 1
        success, image = video_obj.read()
