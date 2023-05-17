import os
import random
import glob
from PIL import Image
import shutil
from pathlib import Path
from ultralytics import YOLO

dir = os.path.dirname(__file__)
model_path = 'yolov8x6.pt'
media_dir = os.path.join(dir, 'media_storage')
detect_dir = os.path.join(dir, 'detect')
source_dir = os.path.join(dir, 'source')
yolo_labels = os.path.join(dir, 'runs', 'predict', 'labels')
yolo_images = os.path.join(dir, 'runs', 'predict')


class Yolo:
    dir = os.path.dirname(__file__)
    model_path = 'yolov8x6.pt'



    def __init__(self):
        self.model = YOLO(model_path)




model = YOLO('yolov8x6.pt')

shutil.rmtree('runs')

results = model.predict(source_dir, save=True, save_txt=True)

labels = glob.glob(f'{yolo_labels}/*.txt')
for label in labels:
    file = open(label, 'r')
    lines = file.read().splitlines()
    file.close()
    for line in lines:
        line = line.split(' ')
        if line[0] == '2':
            file_stem = Path(label).stem
            img_path = f'{yolo_images}/{file_stem}.jpg'
            new_img_path = f'{detect_dir}/{file_stem}.jpg'
            shutil.move(img_path, new_img_path)

shutil.rmtree('runs')