from aiogram import F, Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message, UNSET_PARSE_MODE

from main import dp, bot
from src.buttuns.buttons import main_menu, back_btn

router: Router = Router()


class Form(StatesGroup):
    problem_text = State()
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
    if msg_text == "So'rovni tugatish":
        await message.answer("So'rov tugatildi, bosh menyu", reply_markup=main_menu)
        await state.clear()
    else:
        await message.answer("so'rovingiz yuborildi. Tez orada bog'lanamiz")
        await bot.send_message(chat_id=-1002153624501,
                               text=str(user_id) + " - <b>" + name + "</b>\n\n" + msg_text,
                               parse_mode='html')


def chat_is():
    async def filter(message: Message):
        return message.chat.type in ["supergroup"] and str(message.chat.id) == '-1002153624501'
    return filter


@router.message(chat_is())
async def handling_prob(message: Message):
    if message.reply_to_message and message.reply_to_message.from_user.id == bot.id:
        # Botga reply qilingan

        # Kim reply qilgani haqida ma'lumot
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        username = message.from_user.username

        # Qaysi xabarga reply qilingani haqida ma'lumot
        original_message_id = message.reply_to_message.message_id
        original_message_text = message.reply_to_message.text

        # Reply qilingan xabar matni
        reply_text = message.text
        await bot.send_message(chat_id=original_message_text.split(' - ')[0], text=reply_text)

    else:
        await message.answer("salom")
