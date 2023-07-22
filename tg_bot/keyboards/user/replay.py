from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from tg_bot.data.database import get_buttons


def start_strategy_user():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder=get_buttons()['4'],
        keyboard=[
            [
                KeyboardButton(text=get_buttons()['4'])
            ]
        ]
    )

    return keyboard
