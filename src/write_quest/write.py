import sys
import os
from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, UNSET_PARSE_MODE

from database import cursor, conn
from src.buttuns.buttons import main_menu, back_btn
from config import GROUP_ID, bot

router: Router = Router()


class From(StatesGroup):
    problem_text = State()
    problem_text2 = State()
    problem_file = State()


@router.callback_query()
async def person_quest(call: CallbackQuery, state: FSMContext):
    print(call.data)
    await call.answer()
    await call.message.delete()
    await call.message.answer("Savolingiz matnini yuboring", reply_markup=back_btn)
    await state.set_state(From.problem_text)


@router.message(From.problem_text)
async def person_quest1(message: Message, state: FSMContext):
    msg_text = message.text
    user_id = message.from_user.id
    await state.clear()
    await state.set_state(From.problem_text2)
    if msg_text == "So'rovni tugatish":
        await message.answer("So'rov tugatildi, bosh menyu", reply_markup=main_menu)
        await state.clear()
    else:
        users = cursor.execute("SELECT name, number, region, organization FROM users "
                               f"WHERE user_id='{user_id}';").fetchone()
        if users:
            name, number, region, organization = users
        else:
            name, number, region, organization = None, None, None, None
        msg = await bot.send_message(chat_id=GROUP_ID,
                                     text=(str(user_id) + " - <b>" + name + "</b>\n\n" +
                                           f"Phone: {number}\nRegion: {region}\nTashkilot: {organization}"),
                                     parse_mode='html')
        await bot.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_to_message_id=msg.message_id)


@router.message(From.problem_text2)
async def person_quest1(message: Message, state: FSMContext):
    msg_text = message.text
    user_id = message.from_user.id
    if msg_text == "So'rovni tugatish":
        await message.answer("So'rov tugatildi, bosh menyu", reply_markup=main_menu)
        await state.clear()
    else:
        users = cursor.execute("SELECT name, number, region, organization FROM users "
                               f"WHERE user_id={user_id};").fetchone()
        if users: name, number, region, organization = users
        else: name, number, region, organization = None, None, None, None
        msg = await bot.send_message(chat_id=GROUP_ID,
                                     text=(str(user_id) + " - <b>" + name + "</b>\n\n" +
                                           f"Phone: {number}\nRegion: {region}\nTashkilot: {organization}"),
                                     parse_mode='html')
        await bot.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_to_message_id=msg.message_id)


def chat_is():
    async def filter(message: Message):
        return message.chat.type in ["supergroup"] and message.chat.id == GROUP_ID
    return filter


@router.message(chat_is())
async def handling_prob(message: Message):
    if message.reply_to_message and message.reply_to_message.from_user.id == bot.id:
        original_message_text = message.reply_to_message.text
        try:
            await bot.copy_message(chat_id=original_message_text.split(' - ')[0],
                                   from_chat_id=message.chat.id,
                                   message_id=message.message_id)
        except Exception as ex:
            await message.reply("foydalanuvchiga xabar yuborish uchun uni "
                                "ID va ismi berilgan xabarga javob berish kerak\n\n"
                                "agar siz ID li xabarga javob qilgan bo'lsangiz ammo yana bu xabarni ko'rayotgan "
                                "bo'lsangiz katta extimol siz xabarlashmoqchi bo'lgan user botni blocklagan. "
                                "va unga boshqa xabar yubora olmaysiz")


class Form(StatesGroup):
    name = State()
    phone = State()
    region = State()
    organization = State()


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
    await message.answer("Ismingiz saqlandi. \n\nTelefon nomeringizni yuboring?")


@router.message(Form.phone)
async def save_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(phone=message.text)
    await state.set_state(Form.region)
    await message.answer("Telefon nomeringiz saqlandi. \n\nTashkilotingiz qayerda?")


@router.message(Form.region)
async def save_phone(message: Message, state: FSMContext) -> None:
    await state.update_data(region=message.text)
    await state.set_state(Form.organization)
    await message.answer("Tashkilotingizni nomi nima?")


@router.message(Form.organization)
async def save_phone(message: Message, state: FSMContext) -> None:
    data = await state.update_data(organization=message.text)

    name = data["name"]
    phone = data["phone"]
    region = data["region"]
    organization = message.text

    user_id = message.from_user.id
    users = cursor.execute("select user_id from users").fetchall()
    if user_id not in users:
        cursor.execute(f"INSERT INTO users (user_id, name, number, region, organization) "
                       f"VALUES ({user_id}, '{name}', '{phone}', '{region}', '{organization}')")
        conn.commit()
    await message.answer(text=f"Xush kelibsiz. Davom etishingiz mumkin", reply_markup=main_menu)
    await state.clear()
