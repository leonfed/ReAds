ReAds
================

### Model

You can download the trained model for detection adverts by [link](https://drive.google.com/file/d/1Z6y3wkcviD2MvIGvwqQ1xhHRJNY598Ah/view?usp=sharing).

### Demo

**Run algorithm (advert detection and replacement) on image**
``` bash
python demo_image.py -i input_image.jpg -o output_image.jpg -d detectron_model.pth -b banner.jpg
```

**Run algorithm on video**
``` bash
python demo_video.py -i input_video.mp4 -o output_video.mp4 -d detectron_model.pth -b banner.jpg -p points.tsv -f frames.tsv
```
Paths `points.tsv` and  `frames.tsv` should point to the result, which is obtained using the program [Voodoo](https://www.viscoda.com/index.php/downloads/software).

### Parts of algorithm
The algorithm code consists of the following parts
 - [generation](generation) - generating room 3d-models, which are provided with adverts.
 - [detectron](detectron) - training model Mask R-CNN and using it. We took model [detectron2](https://github.com/facebookresearch/detectron2).
 - [masks](masks) - processing masks, which are obtained as a result of the model Mask R-CNN.
 - [contour](contour) - searching for banner frames using masks.
 - [homography](homography) - embedding a banner on images.
 - [metrics](metrics) - calculation of metrics showing the quality of finding banners on images.
 - [video](video) - video processing scripts.
