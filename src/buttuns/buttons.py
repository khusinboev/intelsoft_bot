from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import cursor, conn

main_menu_kb = [
    # [types.KeyboardButton(text="Kompaniya haqida to'liq ma'lumot")],
    [types.KeyboardButton(text="Muammolar yuzasidan bog'lanish")]
]
main_menu = types.ReplyKeyboardMarkup(keyboard=main_menu_kb, resize_keyboard=True)


products = cursor.execute("select product_name, id from products").fetchall()
products_list = []
for p in products:
    products_list.append([types.InlineKeyboardButton(text=str(p[0]), callback_data=f"{p[1]}")])
products_list.append([types.InlineKeyboardButton(text="Yozma savol berish", callback_data=f"question")])
products_list = InlineKeyboardBuilder(markup=products_list)


back_btn = [[types.KeyboardButton(text="So'rovni tugatish")]]
back_btn = types.ReplyKeyboardMarkup(keyboard=back_btn, resize_keyboard=True)
