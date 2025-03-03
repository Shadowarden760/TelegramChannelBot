import logging
import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(fmt=formatter)
file_handler = logging.FileHandler("logs/bot_log.txt")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(fmt=formatter)
logger.addHandler(file_handler)
logger.addHandler(hdlr=stream_handler)

load_dotenv()


class Settings(BaseSettings):
    DEBUG: bool = True
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    CHAT_ID: str = os.getenv("CHAT_ID")
    WEB_PORT: int = os.getenv("WEB_PORT")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
