import os
import glob
import time
import datetime
import shutil
import asyncio
import re
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from ultralytics import YOLO

from AppConfig import AppConfig

AppConfig = AppConfig()

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
limit_message = 100

processed_mes_id_file_path = os.path.join(DIR_PATH, 'processed_message_id.txt')
log_file_paht = os.path.join(DIR_PATH, 'log.txt')
load_dotenv(DIR_PATH + '/.env')

api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
chat_id = (os.getenv("TARGET_CHAT_ID"))


users_id = [214893352, 319939671]


def get_last_message_id(processed_message_id_file_path):
    file = open(processed_message_id_file_path, 'r')
    lines = file.read().splitlines()
    file.close()
    return int(lines[-1])


def write_processed_mes_id(message_id, processed_message_id_file_path):
    file = open(processed_message_id_file_path, 'a')
    file.write(f'{message_id}\n')
    file.close()


def copy_img(img_file_path=None, target_dir=None):
    img_name = Path(img_file_path).name
    new_img_file_path = os.path.join(target_dir, img_name)
    shutil.copy(img_file_path, new_img_file_path)


def detect_imgs(source_path=None, target_path=None):
    detected_imgs = []
    model = YOLO('yolov8x6.pt')
    model.predict(source_path, save=True, save_txt=True)
    labels = glob.glob(f'{yolo_labels}/*.txt')
    for label in labels:
        file = open(label, 'r')
        lines = file.read().splitlines()
        file.close()
        for line in lines:
            line = line.split(' ')
            if line[0] == str(search_class):
                file_stem = Path(label).stem
                img_path = f'{yolo_images}/{file_stem}.jpg'
                new_img_path = f'{target_path}/{file_stem}.jpg'
                shutil.move(img_path, new_img_path)
                detected_imgs.append(new_img_path)
                break
    return detected_imgs


async def main(last_message_id):
    print(AppConfig.batch_messages)
    source_channel = await client.get_entity(PeerChannel(AppConfig.source_chat_id))

    media_messages_info = []
    count_messages = 0

    async for message in client.iter_messages(source_channel, offset_id=last_message_id, reverse=True):
        if count_messages > AppConfig.batch_messages:
            break
        print(f'Check message {message.id}, {message.date}')
        write_processed_mes_id(message.id, processed_mes_id_file_path)
        count_messages += 1
        if message.media is not None:
            media_file_path = await client.download_media(message, tmp_media_dir)
            if Path(media_file_path).suffix == '.jpg':
                print(f'Save IMG from  message {message.id}')
                media_messages_info.append(
                    [message.id, message.date, message.message, message.from_id, media_file_path]
                )
            else:
                os.remove(media_file_path)

    print(f'Check {count_messages} messages. Media messages - {len(media_messages_info)}')

    return media_messages_info


async def send_file(user_id, img_path):
    await client.send_file(user_id, img_path)


async def send_message(user_id, text):
    await client.send_message(user_id, text)

client = TelegramClient('session', api_id, api_hash)

while True:
    time.sleep(300)
    print('__________ run loop __________')
    if os.path.exists(tmp_media_dir):
        shutil.rmtree(tmp_media_dir)
    os.mkdir(tmp_media_dir)
    if os.path.exists(yolo_runs_dir):
        shutil.rmtree(yolo_runs_dir)

    print('Old dirs deleted, new dirs create.')
    last_message_id = get_last_message_id(processed_mes_id_file_path)
    print(f'Last message id: {last_message_id}')
    with client:
        messages_info = client.loop.run_until_complete(main(last_message_id))

    if not os.listdir(tmp_media_dir):
        print('Do not download new media')
        print('__________ end loop __________')
        continue

    detected_imgs = detect_imgs(source_path=tmp_media_dir, target_path=storage_for_send)

    if not detected_imgs:
        print('Do not detect any obj')
        print('__________ end loop __________')
        continue

    for message in messages_info:
        message_id, message_date, message_message, message_from_id, media_file_path = message
        copy_img(img_file_path=media_file_path, target_dir=storage_for_train)
        source_img_name = Path(media_file_path).name
        for detected_img in detected_imgs:
            detected_img_name = Path(detected_img).name
            if source_img_name == detected_img_name:
                text = f'message_id: {message_id}\n' \
                       f'message_date: {message_date}\n' \
                       f'message_message: {message_message}\n' \
                       f'message_from_id: {message_from_id}\n'
                for user_id in users_id:
                    with client:
                        client.loop.run_until_complete(send_file(user_id, detected_img))
                        client.loop.run_until_complete(send_message(user_id, text))

    print('All messages send')

    print('__________ end loop __________')

