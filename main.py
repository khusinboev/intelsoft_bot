import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message

from config import TOKEN
from src.save_user import save
# from src.problems import problems
# from src.write_quest import write


dp = Dispatcher()
router = Router()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


@router.message()
async def command_start_handler(message: Message) -> None:
    await message.answer(message.video.file_id)
    await bot.send_video(chat_id=message.chat.id,
                         video="BAACAgIAAxkBAAMWZuAoQlWYFHZQFtkdyIVw9VN_kvkAAphaAAL19AABS6S8eKK7OsCDNgQ",
                         caption="Video qo'llanma!")


async def main() -> None:
    dp.include_router(router)
    # dp.include_router(save.router)
    # dp.include_router(problems.router)
    # dp.include_router(write.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
