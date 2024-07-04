from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, UNSET_PARSE_MODE

from config import GROUP_ID
from main import dp, bot
from src.buttuns.buttons import main_menu, back_btn

router: Router = Router()


class Form(StatesGroup):
    problem_text = State()
    problem_text2 = State()
    problem_file = State()


@router.callback_query(F.data == "question")
async def person_quest(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer("Savolingiz matnini yuboring", reply_markup=back_btn)
    await state.set_state(Form.problem_text)


@router.message(Form.problem_text)
async def person_quest1(message: Message, state: FSMContext):
    msg_text = message.text
    user_id = message.from_user.id
    name = message.from_user.full_name
    await state.clear()
    await state.set_state(Form.problem_text2)
    if msg_text == "So'rovni tugatish":
        await message.answer("So'rov tugatildi, bosh menyu", reply_markup=main_menu)
        await state.clear()
    else:
        await message.answer("so'rovingiz yuborildi. Tez orada bog'lanamiz")
        msg = await bot.send_message(chat_id=GROUP_ID,
                                     text=str(user_id) + " - <b>" + name + "</b>\n\n",
                                     parse_mode='html')
        await bot.copy_message(
            chat_id=GROUP_ID,
            from_chat_id=message.chat.id,
            message_id=message.message_id,
            reply_to_message_id=msg.message_id)


@router.message(Form.problem_text2)
async def person_quest1(message: Message, state: FSMContext):
    msg_text = message.text
    user_id = message.from_user.id
    name = message.from_user.full_name
    if msg_text == "So'rovni tugatish":
        await message.answer("So'rov tugatildi, bosh menyu", reply_markup=main_menu)
        await state.clear()
    else:
        msg = await bot.send_message(chat_id=GROUP_ID,
                                     text=str(user_id) + " - <b>" + name + "</b>\n\n",
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
            await bot.forward_message(chat_id=original_message_text.split(' - ')[0],
                                      from_chat_id=message.chat.id,
                                      message_id=message.message_id)
        except Exception as ex:
            print(ex)
            print(original_message_text.split(' - ')[0])
            await message.reply("foydalanuvchiga xabar yuborish uchun uni "
                                "ID va ismi berilgan xabarga javob berish kerak")
