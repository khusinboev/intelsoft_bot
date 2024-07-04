from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from database import cursor, conn
from src.buttuns.buttons import products_list, main_menu

router: Router = Router()


@router.message(F.text == "Muammolar yuzasidan bog'lanish")
async def save_name(message: Message) -> None:
    await message.answer(text="Sizda qaysi maxsulotimiz yuzasidan tushunmovchilik bo'layapti",
                         reply_markup=products_list.as_markup())


def get_buttons_from_db():
    async def filter(callback: CallbackQuery):
        try:
            products = [prod[0] for prod in cursor.execute("select id from products").fetchall()]
            return int(callback.data) in products
        except:
            return False
    return filter


@router.callback_query(get_buttons_from_db())
async def save_name(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.delete()
    await call.message.answer("mana sizning problemingizni yechimi", reply_markup=main_menu)
