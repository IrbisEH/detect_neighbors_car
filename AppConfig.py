import os

from dotenv import load_dotenv


def check_and_load_env():
    if os.path.exists('.env'):
        load_dotenv('.env')
    else:
        print('В основной диерктории отсутствует .env')
        exit()


class AppConfig:
    def __init__(self):
        check_and_load_env()
        # dir and file paths
        self.dir_path = os.getenv('DIR_PATH', os.path.dirname(__file__))
        self.media_storage_path = os.path.join(self.dir_path, 'media_storage')
        self.storage_for_train_path = os.path.join(self.media_storage_path, 'storage_for_train')
        self.storage_for_send_path = os.path.join(self.media_storage_path, 'storage_for_send')
        self.storage_tmp_path = os.path.join(self.media_storage_path, 'tmp')
        self.processed_message_id_file_path = os.path.join(self.dir_path, 'processed_message_id.txt')
        # yolo app dir paths
        self.model_path = os.path.join(self.dir_path, 'yolov8x6.pt')
        self.yolo_runs_dir_path = os.path.join(self.dir_path, 'runs')
        self.yolo_labels_dir_path = os.path.join(self.yolo_runs_dir_path, 'detect', 'predict', 'labels')
        self.yolo_images_dir_path = os.path.join(self.yolo_runs_dir_path, 'detect', 'predict')
        # yolo configs
        self.search_class_ids = {
            'car': 2,
            # 'truck':
        }
        self.yolo_conf_img = 1280
        # tg configs
        self.api_id = int(os.getenv('API_ID'))
        self.api_hash = str(os.getenv('API_HASH'))
        self.bot_token = str(os.getenv('BOT_API_KEY'))
        self.source_chat_id = int(os.getenv('SOURCE_CHAT_ID'))
        self.send_to_user_ids = {
            'me': 214893352,
            'sasha': 319939671
        }
        self.batch_messages = 100
        self.sleep_time = 300       # seconds
