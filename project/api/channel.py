from typing import Optional

from fastapi import APIRouter, HTTPException, status, UploadFile, File

from bot.bot_client import BotClient
from config import get_settings

settings = get_settings()

router = APIRouter()


@router.post(path="/configure_channel", name="channel:configure")
async def configure_channel(new_channel_title: Optional[str] = None, new_channel_description: Optional[str] = None,
                            photo: UploadFile = None) -> dict:
    try:
        bot = BotClient(bot_token=settings.BOT_TOKEN, chat_id=settings.CHAT_ID, debug=settings.DEBUG)
        await bot.configure_channel(
            new_channel_title=new_channel_title,
            new_channel_description=new_channel_description,
            new_channel_photo=photo.file.read() if photo is not None else None
        )
        return {"status": "ok"}
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ex}"
        )

@router.post(path="/send_text_message", name="channel:send_text_message")
async def send_text_message(message_text: str) -> dict:
    try:
        bot = BotClient(bot_token=settings.BOT_TOKEN, chat_id=settings.CHAT_ID, debug=settings.DEBUG)
        await bot.send_text_message(text=message_text)
        return {"status": "ok"}
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ex}"
        )

@router.post(path="/send_photo_message", name="channel:send_photo_message")
async def send_photo_message(photo: UploadFile, caption: Optional[str] = None) -> dict:
    try:
        bot = BotClient(bot_token=settings.BOT_TOKEN, chat_id=settings.CHAT_ID, debug=settings.DEBUG)
        await bot.send_photo_message(photo=photo.file.read(),caption=caption)
        return {"status": "ok"}
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ex}"
        )

@router.post(path="/delete_message", name="channel:delete_message")
async def delete_text_message(message_id: int) -> dict:
    try:
        bot = BotClient(bot_token=settings.BOT_TOKEN, chat_id=settings.CHAT_ID, debug=settings.DEBUG)
        await bot.delete_message(message_id=message_id)
        return {"status": "ok"}
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{ex}"
        )