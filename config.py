from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message


from pathlib import Path

BASE_DIR = str(Path(__file__).resolve().parent)

TOKEN = "7470635147:AAEM6Z1K7CKD2LDBZ9vTAs7fWUsoqsIldDM"
GROUP_ID = -1002153624501
DB_NAME = BASE_DIR + '/intel_soft.db'

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))