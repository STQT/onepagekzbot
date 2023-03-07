from aiogram import types


def main_page_button() -> types.InlineKeyboardMarkup:
    keyboard_markup = types.InlineKeyboardMarkup(row_width=1)
    keyboard_markup.add(types.InlineKeyboardButton("На главную", callback_data='main_page'))
    return keyboard_markup
