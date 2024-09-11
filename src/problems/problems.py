from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaVideo

from config import bot
from database import cursor, conn
from src.buttuns.buttons import products_list, main_menu

router: Router = Router()


@router.message(F.text == "Muammolar yuzasidan bog'lanish")
async def save_name(message: Message) -> None:
    await message.answer(text="Sizda qaysi maxsulotimiz yuzasidan tushunmovchilik bo'layapti",
                         reply_markup=products_list.as_markup())


@router.callback_query(F.data == "2")
async def save_name(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.delete()
    await bot.send_media_group(chat_id=call.message.chat.id,
                               media=[InputMediaVideo(
                                   media="BAACAgIAAxkBAAMWZuAoQlWYFHZQFtkdyIVw9VN_kvkAAphaAAL19AABS6S8eKK7OsCDNgQ",
                                   caption="Ekran va urollarni kalibrovka qilish bo'yicha video qo'llanmalar"),
                                   InputMediaVideo(
                                       media="BAACAgIAAxkBAANWZuGHco_ZHYmk2voJri3bri2seh4AAmdWAAJMzwhLWg6B8aVZdL02BA")])
