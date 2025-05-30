from typing import Union

import telegram

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
            self.__save_logs(
                BotLogModel(
                    status=True,
                    action=action,
                    data= {"message_id": message.message_id, "message_text": message.text }
                )
            )
            return True
        except Exception as ex:
            self.__save_logs(
                BotLogModel(
                    status=False,
                    action=action,
                    data={"error": ex}
                )
            )
            return False

    async def send_photo_message(self, photo: bytes, caption: Union[str, None] = None) -> bool:
        action = BotClient.send_photo_message.__name__
        try:
            if caption is not None and len(caption) < telegram.constants.MessageLimit.CAPTION_LENGTH:
                message = await self.__bot.send_photo(chat_id=self.__chat_id, caption=caption, photo=photo)
            else:
                message = await self.__bot.send_photo(chat_id=self.__chat_id, photo=photo)
            self.__save_logs(
                BotLogModel(
                    status=True,
                    action=action,
                    data={"message_id": message.message_id, "message_text": message.text}
                )
            )
            return True
        except Exception as ex:
            self.__save_logs(
                BotLogModel(
                    status=False,
                    action=action,
                    data={"error": ex}
                )
            )
            return False

    async def delete_message(self, message_id: int):
        action = BotClient.delete_message.__name__
        try:
            status = await self.__bot.delete_message(chat_id=self.__chat_id, message_id=message_id)
            self.__save_logs(
                BotLogModel(
                    status=status,
                    action=action,
                    data={"message_id": message_id}
                )
            )
            return True
        except Exception as ex:
            self.__save_logs(
                BotLogModel(
                    status=False,
                    action=action,
                    data={"error": ex}
                )
            )
            return False

    async def configure_channel(self, new_channel_title: Union[str, None] = None,
                                new_channel_description: Union[str, None] = None,
                                new_channel_photo: Union[bytes, None] = None):
        action = BotClient.configure_channel.__name__
        try:
            if new_channel_title is not None and telegram.constants.ChatLimit.MIN_CHAT_TITLE_LENGTH <= len(
                    new_channel_title) <= telegram.constants.ChatLimit.MAX_CHAT_TITLE_LENGTH:
                title_status = await self.__bot.set_chat_title(chat_id=self.__chat_id, title=new_channel_title)
                self.__save_logs(
                    BotLogModel(
                        status=title_status,
                        action=action,
                        data={"new_title": new_channel_title}
                    )
                )
            if new_channel_description is not None and telegram.constants.ChatLimit.CHAT_DESCRIPTION_LENGTH > len(
                    new_channel_description):
                description_status = await self.__bot.set_chat_description(chat_id=self.__chat_id,
                                                                           description=new_channel_description)
                self.__save_logs(
                    BotLogModel(
                        status=description_status,
                        action=action,
                        data={"new_description": new_channel_description}
                    )
                )
            if new_channel_photo is not None:
                photo_status = await self.__bot.set_chat_photo(chat_id=self.__chat_id, photo=new_channel_photo)
                self.__save_logs(
                    BotLogModel(
                        status=photo_status,
                        action=action,
                        data={"new_photo": new_channel_photo}
                    )
                )
            return True
        except Exception as ex:
            self.__save_logs(
                BotLogModel(
                    status=False,
                    action=action,
                    data={"error": ex}
                )
            )
            return False

    async def create_new_admin(self, user_id: int) -> bool:
        action = BotClient.create_new_admin.__name__
        status =  await self.__bot.promote_chat_member(
            chat_id=self.__chat_id,
            user_id=user_id,
            can_post_messages=True,
            can_edit_messages=True,
            can_delete_messages=True,
            can_pin_messages=True,
            can_manage_video_chats=True,
            can_manage_topics=True,
            can_post_stories=True,
            can_edit_stories=True,
            can_delete_stories=True
        )
        self.__save_logs(
            BotLogModel(
                status=status,
                action=action,
                data={"user_id": user_id}
            )
        )
        return status

    async def get_channel_stat(self) -> dict:
        action = BotClient.get_channel_stat.__name__
        data = {
            "members_count": str(await self.__bot.get_chat_member_count(chat_id=self.__chat_id)),
            "admins": str(await self.__bot.get_chat_administrators(chat_id=self.__chat_id))
        }
        self.__save_logs(
            BotLogModel(
                status=True,
                action=action,
                data=data
            )
        )
        return data

    def __save_logs(self, bot_log: BotLogModel):
        if self.__debug:
            logger.info(bot_log.model_dump_json())
