from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_admin():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Главное меню админа 👀',
        keyboard=[
            [
                KeyboardButton(text='🔒 Пароль')
            ],
            [
                KeyboardButton(text='💬 Сообщения'),
                KeyboardButton(text='📌 Кнопки')
            ]
        ]
    )

    return keyboard