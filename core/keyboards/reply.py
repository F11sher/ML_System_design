from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard(text):
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text=text)

    keyboard_builder.adjust(1)

    return keyboard_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
