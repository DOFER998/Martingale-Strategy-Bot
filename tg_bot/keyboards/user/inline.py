from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.data.database import get_buttons


def choice_user_stake(amount, coeff):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=get_buttons()['1'], callback_data=f"winning:{amount}:{coeff}"),
            InlineKeyboardButton(text=get_buttons()['2'], callback_data=f"losing:{amount}:{coeff}")
        ],
        [
            InlineKeyboardButton(text=get_buttons()['3'], callback_data="stop")
        ]
    ])
    return keyboard