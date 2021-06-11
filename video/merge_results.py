import os

from PIL import Image

# помещает два изображения рядом с друг с другом в одно jpg
if __name__ == "__main__":
    files = os.listdir('data/processed_images')
    files = list(map(lambda x: x.split('.')[0], files))
    print(len(files))

    for filename in files:
        print(filename)
        path1 = 'data/input/%s.jpg' % filename
        path2 = 'data/processed_images/%s.jpg' % filename

        img1 = Image.open(path1)
        img2 = Image.open(path2)

        image_width = img1.size[0]
        image_height = img1.size[1]

        res_width = image_width * 2
        res_height = int(image_height * 2.05)
        res_img = Image.new('RGB', (res_width, res_height))

        paste_width = int(res_width * 0.32)
        res_img.paste(img1, (paste_width, 0))
        res_img.paste(img2, (paste_width, res_height - image_height))

        res_img.save("data/final_result/%s.jpg" % filename)
