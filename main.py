import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from src.save_user import save
from src.problems import problems
from src.write_quest import write

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "5597490636:AAHiyobYfWKIqdzd8CDPzHoaZes5EiWr1pw"
dp = Dispatcher()
router = Router()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    dp.include_router(router)
    dp.include_router(save.router)
    dp.include_router(problems.router)
    dp.include_router(write.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
