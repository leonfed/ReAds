import os

from PIL import Image

# помещает два изображения рядом с друг с другом в одно jpg
if __name__ == "__main__":
    files = os.listdir('data/processed_images_v2')
    files = list(map(lambda x: x.split('.')[0], files))
    print(len(files))

    for filename in files:
        print(filename)
        path1 = 'data/input/%s.jpg' % filename
        path2 = 'data/processed_images_v2/%s.jpg' % filename

        img1 = Image.open(path1)
        img2 = Image.open(path2)

        image_width = img1.size[0]
        image_height = img1.size[1]

        res_width = int(image_width * 2.05)
        res_height = image_height * 2
        res_img = Image.new('RGB', (res_width, res_height))

        paste_height = int(res_height * 0.25)
        res_img.paste(img1, (0, paste_height))
        res_img.paste(img2, (res_width - image_width, paste_height))

        res_img.save("data/final_result/%s.jpg" % filename)
