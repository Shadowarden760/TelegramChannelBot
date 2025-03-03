from pathlib import Path

import telegram
from typing import Union
from project.bot.models import BotLogModel
from project.config import logger


class BotClient:

    def __init__(self, bot_token: str, chat_id: str, debug: bool = False):
        self.__debug = debug
        self.__bot_token = bot_token
        self.__chat_id = chat_id
        self.__bot = telegram.Bot(token=self.__bot_token)

    async def send_text_message(self, text: str) -> bool:
        action = BotClient.send_text_message.__name__
        try:
            if len(text) > telegram.constants.MessageLimit.MAX_TEXT_LENGTH:
                return False
            message = await self.__bot.send_message(chat_id=self.__chat_id, text=text)
            self.__save_logs(BotLogModel(
                message_id=message.message_id,
                message_text=message.text,
                action=action,
                status=True
            ))
            return True
        except Exception as ex:
            self.__save_logs(BotLogModel(
                message_text=str(ex),
                action=action,
                status=False
            ))
            return False

    async def send_photo_message(self, photo: bytes, caption: Union[str, None] = None) -> bool:
        action = BotClient.send_photo_message.__name__
        try:
            if caption is not None and len(caption) < telegram.constants.MessageLimit.CAPTION_LENGTH:
                message = await self.__bot.send_photo(chat_id=self.__chat_id, caption=caption, photo=photo)
            else:
                message = await self.__bot.send_photo(chat_id=self.__chat_id, photo=photo)
            self.__save_logs(BotLogModel(
                message_id=message.message_id,
                message_text=message.text,
                action=action,
                status=True
            ))
            return True
        except Exception as ex:
            self.__save_logs(BotLogModel(
                message_text=str(ex),
                action=action,
                status=False
            ))
            return False

    async def delete_message(self, message_id: int):
        action = BotClient.delete_message.__name__
        try:
            status = await self.__bot.delete_message(chat_id=self.__chat_id, message_id=message_id)
            self.__save_logs(BotLogModel(
                action=action,
                status=status
            ))
            return True
        except Exception as ex:
            self.__save_logs(BotLogModel(
                message_text=str(ex),
                action=action,
                status=False
            ))
            return False

    async def configure_channel(self, new_channel_title: Union[str, None] = None,
                                new_channel_description: Union[str, None] = None,
                                new_channel_photo: Union[bytes, None] = None):
        action = BotClient.configure_channel.__name__
        try:
            if new_channel_title is not None and telegram.constants.ChatLimit.MIN_CHAT_TITLE_LENGTH <= len(
                    new_channel_title) <= telegram.constants.ChatLimit.MAX_CHAT_TITLE_LENGTH:
                title_status = await self.__bot.set_chat_title(chat_id=self.__chat_id, title=new_channel_title)
                self.__save_logs(BotLogModel(
                    message_text="configurate title",
                    action=action,
                    status=title_status
                ))
            if new_channel_description is not None and telegram.constants.ChatLimit.CHAT_DESCRIPTION_LENGTH > len(
                    new_channel_description):
                description_status = await self.__bot.set_chat_description(chat_id=self.__chat_id,
                                                                           description=new_channel_description)
                self.__save_logs(BotLogModel(
                    message_text="configurate description",
                    action=action,
                    status=description_status
                ))
            if new_channel_photo is not None:
                photo_status = await self.__bot.set_chat_photo(chat_id=self.__chat_id, photo=new_channel_photo)
                self.__save_logs(BotLogModel(
                    message_text="configurate photo",
                    action=action,
                    status=photo_status
                ))
            return True
        except Exception as ex:
            self.__save_logs(BotLogModel(
                message_text=str(ex),
                action=action,
                status=False
            ))
            return False

    def __save_logs(self, bot_log: BotLogModel):
        if self.__debug:
            logger.info(bot_log.model_dump_json())
