# Прежде всего необходимо установить нужные пакеты
# !pip install pyyaml==5.1
# !pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.8/index.html

import numpy as np
import os, json, cv2

import torch, torchvision
import detectron2

from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import BoxMode
from detectron2.engine import HookBase
from detectron2.engine import DefaultTrainer


def get_banner_dicts(main_dir):
    setup_logger()

    dataset_dicts = []
    img_dir = main_dir
    json_file = os.path.join(img_dir, "via_region_data.json")
    with open(json_file) as f:
        imgs_anns = json.load(f)

    for idx, v in enumerate(imgs_anns.values()):
        record = {}

        filename = os.path.join(img_dir, v["filename"])
        height, width = cv2.imread(filename).shape[:2]

        record["file_name"] = filename
        record["image_id"] = idx
        record["height"] = height
        record["width"] = width

        annos = v["regions"]
        objs = []
        for _, anno in annos.items():
            anno = anno["shape_attributes"]
            px = anno["all_points_x"]
            py = anno["all_points_y"]
            poly = [(x + 0.5, y + 0.5) for x, y in zip(px, py)]
            poly = [p for x in poly for p in x]

            obj = {
                "bbox": [np.min(px), np.min(py), np.max(px), np.max(py)],
                "bbox_mode": BoxMode.XYXY_ABS,
                "segmentation": [poly],
                "category_id": 0,
            }
            objs.append(obj)
        record["annotations"] = objs
        dataset_dicts.append(record)
    return dataset_dicts


# Для логгирования номера текущей итерации
class IterationHook(HookBase):
    def after_step(self):
        print(f"Iteration {self.trainer.iter}!")


# Обучает модель
if __name__ == "__main__":
    dataset_path = "detectron_train_data/"

    DatasetCatalog.register("banner", get_banner_dicts(dataset_path))
    MetadataCatalog.get("banner").set(thing_classes=["banner"])
    banners_metadata = MetadataCatalog.get("banner")

    dataset_dicts = get_banner_dicts("detectron_train_data/")

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

    # создаем директорию, куда поместим обученную модель
    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)

    # Обучаем
    trainer = DefaultTrainer(cfg)
    trainer.resume_or_load(resume=False)
    trainer.register_hooks([IterationHook()])
    trainer.train()
