from aiogram import html, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from database import cursor, conn
from src.buttuns.buttons import main_menu
router: Router = Router()


class Form(StatesGroup):
    name = State()
    phone = State()


@router.message(CommandStart())
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


