import os
import glob
import time
import datetime
import shutil
import re
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from ultralytics import YOLO


DIR_PATH = os.path.dirname(__file__)
media_storage = os.path.join(DIR_PATH, 'media_storage')
storage_for_train = os.path.join(media_storage, 'storage_for_train')
storage_for_send = os.path.join(media_storage, 'storage_for_send')
tmp_media_dir = os.path.join(media_storage, 'tmp')

model_path = 'yolov8x6.pt'
yolo_runs_dir = os.path.join(DIR_PATH, 'runs')
yolo_labels = os.path.join(yolo_runs_dir, 'detect', 'predict', 'labels')
yolo_images = os.path.join(yolo_runs_dir, 'detect', 'predict')
search_class = 2

processed_mes_id_file_path = os.path.join(DIR_PATH, 'processed_message_id.txt')
log_file_paht = os.path.join(DIR_PATH, 'log.txt')
load_dotenv(DIR_PATH + '/.env')

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
chat_id = int(os.getenv("TARGET_CHAT_ID"))

users_id = [214893352, 319939671]

client = TelegramClient('session', api_id, api_hash)

async def send_file(user_id):
    await client.send_file(user_id, '/home/irbis-eh/Desktop/detect_neighbors_car/media_storage/storage_for_send/photo_2023-01-21_15-05-29.jpg')

for user in users_id:
    with client:
        client.loop.run_until_complete(send_file(user))