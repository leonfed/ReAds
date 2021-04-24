# Прежде всего необходимо установить нужные пакеты
# !pip install pyyaml==5.1
# !pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.8/index.html

import numpy as np
import os, cv2

import torch, torchvision
import detectron2

from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog

# Используем обученную модель
if __name__ == "__main__":
    setup_logger()

    model_path = "detectron_model.pth"
    test_data_path = "detectron_test_data/"
    result_path = "test_output/"

    # Настраиваем
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg.DATASETS.TRAIN = ("banner",)
    cfg.DATASETS.TEST = ()
    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.00025
    cfg.SOLVER.MAX_ITER = 1300
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 1
    cfg.MODEL.WEIGHTS = model_path
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    predictor = DefaultPredictor(cfg)

    files = os.listdir(test_data_path)
    files = list(filter(lambda x: not x.endswith('csv'), files))
    print(files)

    for file in files:
        print(file)
        im = cv2.imread(test_data_path + file)
        outputs = predictor(im)
        v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        out.save(result_path + file)
        masks = outputs["instances"].to("cpu").pred_masks
        np.save(result_path + file.split('.')[0], masks.numpy())
        scores = outputs["instances"].to("cpu").scores
        np.save(result_path + "scores_" + file.split('.')[0], scores.numpy())
