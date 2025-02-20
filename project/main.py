import asyncio
import pathlib

from bot_utils.bot_client import BotClient
from config import get_settings

settings = get_settings()


async def main():
    my_bot = BotClient(bot_token=settings.BOT_TOKEN, chat_id=settings.CHAT_ID, debug=settings.DEBUG)
    await my_bot.configure_channel(
        new_chat_title="your channel name",
        new_channel_description="your channel description",
        new_channel_photo=pathlib.Path("images/test_image.jpg")
    )
    # await my_bot.send_text_message(text="Some test message")


if __name__ == "__main__":
    asyncio.run(main())
