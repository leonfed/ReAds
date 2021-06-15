import argparse

from contour.composition import compostion_find
from detectron.use_detectron import detect
from homography.replace import replace_banner
from masks.choose_mask import choose

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--imagePath", default="image.jpg", help="Path to the image")
    parser.add_argument("-o", "--outputPath", default="output.jpg", help="Path to store the result")
    parser.add_argument("-d", "--detectronPath", default="detectron_model.pth", help="Path to detectron model")
    parser.add_argument("-b", "--newBannerPath", default="banner.jpg", help="Path to new banner")
    args = parser.parse_args()
    detectron_path = args.detectronPath
    image_path = args.imagePath
    new_banner_path = args.newBannerPath
    output_path = args.outputPath

    # нахождение масок баннера
    masks_path = "tmp_masks.npy"
    scores_path = "tmp_scores.npy"
    detect(detectron_path, image_path, masks_path, scores_path)

    # выбрать одну маску
    final_mask_path = "tmp_final_mask.npy"
    is_chosen = choose(masks_path, scores_path, final_mask_path)
    if not is_chosen:
        print("Detection is failed")
        exit()

    # находим рамки баннера
    contour_path = compostion_find(image_path, final_mask_path)

    # заменить баннер
    replace_banner(new_banner_path, image_path, contour_path, output_path)
