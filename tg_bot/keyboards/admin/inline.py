from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.data.database import get_buttons


def message_page(page: int = 1):
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="✏ Редактировать",
                                                                 callback_data=f"edit_message:{page}"),
                                        ],
                                        [
                                            InlineKeyboardButton(text="⬅ Назад",
                                                                 callback_data=f"negative_message:{page - 1}"),
                                            InlineKeyboardButton(text=f"| {page}/7 |",
                                                                 callback_data="dont_click_me"),
                                            InlineKeyboardButton(text="Вперёд ➡",
                                                                 callback_data=f"plus_message:{page + 1}")
                                        ]
                                    ])

    return keyboard


def buttons_edit():
    button = get_buttons()
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=button['1'], callback_data="buttons_edit:1"),
                                        ],
                                        [
                                            InlineKeyboardButton(text=button['2'], callback_data="buttons_edit:2"),
                                            InlineKeyboardButton(text=button['3'], callback_data="buttons_edit:3"),
                                            InlineKeyboardButton(text=button['4'], callback_data="buttons_edit:4")
                                        ]
                                    ])

    return keyboard


def pass_edit():
    keyboard = InlineKeyboardMarkup(row_width=2,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="✏ Редактировать", callback_data="edit_pass"),
                                        ],
                                    ])

    return keyboard
