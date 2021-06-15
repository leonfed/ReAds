import argparse
import os
import shutil
from PIL import Image
import cv2

from contour.composition import compostion_find
from detectron.use_detectron import detect
from homography.replace import replace_banner
from masks.choose_mask import choose
from video.voodoo_contours import expand_contours

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--videoPath", default="video.mp4", help="Path to the video")
    parser.add_argument("-o", "--outputPath", default="output.mp4", help="Path to store the result")
    parser.add_argument("-d", "--detectronPath", default="detectron_model.pth", help="Path to detectron model")
    parser.add_argument("-b", "--newBannerPath", default="banner.jpg", help="Path to new banner")
    parser.add_argument("-p", "--points", default="points.tsv", help="Path to 3d-model's points of video scene")
    parser.add_argument("-f", "--framesParams", default="frames.tsv", help="Path to frame params")
    args = parser.parse_args()
    detectron_path = args.detectronPath
    video_path = args.videoPath
    new_banner_path = args.newBannerPath
    output_path = args.outputPath
    points_3d_path = args.points
    frames_params_path = args.framesParams

    # создаем рабочую директорию
    tmp_dir = ".ads_tmp/"
    frames_dir = tmp_dir + "frames/"
    contours_dir = tmp_dir + "frames/"
    result_dir = tmp_dir + "result_frames/"
    for new_dir in [tmp_dir, frames_dir, contours_dir, result_dir]:
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)

    # рабить видео на кадры
    video_obj = cv2.VideoCapture(video_path)
    frames_count = 0
    success, image = video_obj.read()
    while success:
        cv2.imwrite(frames_dir + str(frames_count) + ".jpg", image)
        frames_count += 1
        success, image = video_obj.read()

    if frames_count == 0:
        print("Video is empty")
        exit()

    # прогнать детектроном первый кадр
    first_frame_path = frames_dir + '0.jpg'
    masks_path = "tmp_masks.npy"
    scores_path = "tmp_scores.npy"
    detect(detectron_path, first_frame_path, masks_path, scores_path)

    # выбрать одну маску
    first_frame_mask_path = "tmp_final_mask.npy"
    is_chosen = choose(masks_path, scores_path, first_frame_mask_path)
    if not is_chosen:
        print("Detection is failed")
        exit()

    # находим рамки баннера
    contour_path = compostion_find(first_frame_path, first_frame_mask_path)
    shutil.copy(contour_path, contours_dir + "0.npy")

    # найти контуры на оставшихся кадрах
    expand_contours(contours_dir, frames_params_path, points_3d_path, frames_count)

    # заменить баннер на кадрах
    for i in range(frames_count):
        input_path = frames_dir + str(i) + ".jpg"
        contour_path = contours_dir + str(i) + ".npy"
        result_path = result_dir + str(i) + ".jpg"
        replace_banner(new_banner_path, input_path, contour_path, result_path)

    # собрать кадры в видео
    image = Image.open(result_dir + "0.jpg")
    frame_width = image.size[0]
    frame_height = image.size[1]

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 24, (frame_width, frame_height))

    for i in range(frames_count):
        path = result_dir + str(i) + ".jpg"
        frame = cv2.imread(path)
        out.write(frame)

    out.release()
