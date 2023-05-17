import os
import glob
import time
import datetime
import shutil
import re
import asyncio
from tqdm import tqdm
from pathlib import Path
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
from ultralytics import YOLO

from AppConfig import AppConfig

Conf = AppConfig()
client = TelegramClient('session', Conf.api_id, Conf.api_hash)
client.start()
