ReAds
================

Программная часть диплома.

Тема диплома:  __"Вписывание баннеров рекламного характера в видео методами компьютерного зрения"__

### Модель

Скачать обученную модель детекции рекламные баннером можно по [ссылке](https://drive.google.com/file/d/1Z6y3wkcviD2MvIGvwqQ1xhHRJNY598Ah/view?usp=sharing).

### Демо

**Для запуска обработки баннера (его детекция и замена) можно выполнить команду**
``` bash
python demo_image.py -i input_image.jpg -o output_image.jpg -d detectron_model.pth -b banner.jpg
```

**Для запуска обработки видео можно выполнить команду**
``` bash
python demo_video.py -i input_video.mp4 -o output_video.mp4 -d detectron_model.pth -b banner.jpg -p points.tsv -f frames.tsv
```
Пути `points.tsv` и  `frames.tsv` должны указывать на результат, полученный после обработки видео алгоритммом [Voodoo](https://www.viscoda.com/index.php/downloads/software).

### Составляющие алгоритма
Алгоритм разбит на части:
 - [generation](generation) - генерация 3d-моделей комнат, с помещенными в них баннерами, а также создание скриншотов моделей с баннерами.
 - [detectron](detectron) - обучение модели Mask R-CNN и ее использование. Использована модель [detectron2](https://github.com/facebookresearch/detectron2).
 - [masks](masks) - обработка масок, полученных в результате работы модели Mask R-CNN.
 - [contour](contour) - алгоритмы для нахождения рамок баннеров с использованием масок.
 - [homography](homography) - вписывание баннера в изображения.
 - [metrics](metrics) - подсчет метрик, показывающих качество нахождения баннеров на изображениях.
 - [video](video) - скрипты для работы с видео.
