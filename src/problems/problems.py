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


def get_buttons_from_db():
    async def filter(callback: CallbackQuery):
        # try:
        #     products = [prod[0] for prod in cursor.execute("select id from products").fetchall()]
        #     return int(callback.data) in products
        # except:
        #     return False
        if callback.data == "tir": return True
        else: return False
    return filter


@router.callback_query(get_buttons_from_db())
async def save_name(call: CallbackQuery) -> None:
    await call.answer()
    await call.message.delete()
    await bot.send_media_group(chat_id=call.message.chat.id,
                               media=[InputMediaVideo(
                                   media="BAACAgIAAxkBAAMWZuAoQlWYFHZQFtkdyIVw9VN_kvkAAphaAAL19AABS6S8eKK7OsCDNgQ",
                                   caption="Ekran va urollarni kalibrovka qilish bo'yicha video qo'llanmalar"),
                                   InputMediaVideo(
                                       media="BAACAgIAAxkBAANWZuGHco_ZHYmk2voJri3bri2seh4AAmdWAAJMzwhLWg6B8aVZdL02BA")])

    # await call.message.answer("Mana sizning problemingizni yechimi", reply_markup=main_menu)


class Form(StatesGroup):
    name = State()
    phone = State()


@router.message()
async def command_start_handler(message: Message, state: FSMContext) -> None:
    try:
        await state.clear()
    except:
        pass
    user_id = message.from_user.id
    users = [idd[0] for idd in cursor.execute("select user_id from users").fetchall()]

    if message.chat.type in ['supergroup']:
        pass
    elif user_id not in users:
        await state.set_state(Form.name)
        await message.answer(f"Ismingizni kitiring?")
    else:
        await message.answer("Assalomu alaykum, xush kelibsiz. Davom etishingiz mumkin", reply_markup=main_menu)


@router.message(Form.name)
async def save_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.phone)
    await message.answer("Ismingiz saqlandi. \n\nTelefon nomeringizni yuboring")


@router.message(Form.phone)
async def save_phone(message: Message, state: FSMContext) -> None:
    data = await state.update_data(language=message.text)
    name = data["name"]
    phone = message.text
    user_id = message.from_user.id
    users = cursor.execute("select user_id from users").fetchall()
    if user_id not in users:
        cursor.execute(f"INSERT INTO users (user_id, name, number) VALUES ({user_id}, '{name}', '{phone}')")
        conn.commit()
    await message.answer(text=f"Xush kelibsiz. Davom etishingiz mumkin", reply_markup=main_menu)
    await state.clear()
