from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tg_bot.data.database import get_password, get_messages, edit_message_db, edit_button_db, edit_pass_db, get_pass
from tg_bot.data.config import ADMIN
from tg_bot.data.loader import bot
from tg_bot.filters.is_admin import IsAdmin
from tg_bot.keyboards.admin.inline import message_page, buttons_edit, pass_edit
from tg_bot.keyboards.admin.replay import main_menu_admin
from tg_bot.misc.states import EditMessage, EditButton, EditPass

router = Router(name="User main router")
router.message.filter(F.chat.type == "private")


@router.message(IsAdmin(user=ADMIN), Command(commands=['admin_menu']))
async def admin_menu(message: Message):
    await message.answer(text='<b>👁 Меню админа</b>', reply_markup=main_menu_admin())


@router.message(IsAdmin(user=ADMIN), F.text == '💬 Сообщения')
async def admin_menu_messages(message: Message):
    messages = get_messages()
    await message.answer(text=f'<b>💬 Сообщение №1</b>{messages["1"]}', reply_markup=message_page())


@router.callback_query(F.data.startswith('negative_message:'))
async def negative_message(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    try:
        messages = get_messages()
        await call.message.edit_text(text=f'<b>💬 Сообщение №{page}</b>\n\n{messages[str(page)]}',
                                     reply_markup=message_page(page))
    except Exception:
        await call.answer(text='⚠ Листай вперед')


@router.callback_query(F.data.startswith('plus_message:'))
async def plus_message(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    try:
        messages = get_messages()
        await call.message.edit_text(text=f'<b>💬 Сообщение №{page}</b>\n\n{messages[str(page)]}',
                                     reply_markup=message_page(page))
    except Exception:
        await call.answer(text='⚠ Листай назад')


@router.callback_query(F.data.startswith('edit_message:'))
async def edit_message(call: CallbackQuery, state: FSMContext):
    msg = int(call.data.split(":")[1])
    await call.message.edit_text(text='✏ Введите текст для замены')
    await state.set_state(EditMessage.edit_message)
    await state.update_data(edit=call.message.message_id, message=msg)


@router.message(F.text, EditMessage.edit_message)
async def edit_message_next(message: Message, state: FSMContext):
    answer = message.text
    await message.delete()
    data = await state.get_data()
    edit_message_db(_id=str(data["message"]), message=answer)
    messages = get_messages()
    await bot.edit_message_text(chat_id=message.chat.id, message_id=data['edit'],
                                text=f'<b>💬 Сообщение №{data["message"]}</b>\n\n{messages[str(data["message"])]}',
                                reply_markup=message_page(int(data["message"])))
    await state.clear()


@router.message(IsAdmin(user=ADMIN), F.text == '📌 Кнопки')
async def admin_menu_buttons(message: Message):
    await message.answer(text=f'<b>📌 Кнопки</b>', reply_markup=buttons_edit())


@router.callback_query(F.data.startswith('buttons_edit:'))
async def edit_button(call: CallbackQuery, state: FSMContext):
    but = int(call.data.split(":")[1])
    await call.message.edit_text(text='✏ Введите текст для замены')
    await state.set_state(EditButton.edit_button)
    await state.update_data(edit=call.message.message_id, button=but)


@router.message(F.text, EditButton.edit_button)
async def edit_button_next(message: Message, state: FSMContext):
    answer = message.text
    await message.delete()
    data = await state.get_data()
    edit_button_db(_id=str(data["button"]), message=answer)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=data['edit'], text=f'<b>📌 Кнопки</b>',
                                reply_markup=buttons_edit())
    await state.clear()


@router.message(IsAdmin(user=ADMIN), F.text == '🔒 Пароль')
async def admin_menu_pass(message: Message):
    await message.answer(text=f'<b>🔒 Пароль</b>\n\n<tg-spoiler>{get_pass()}</tg-spoiler>', reply_markup=pass_edit())


@router.callback_query(F.data == 'edit_pass')
async def edit_pass(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text='✏ Введите текст для замены')
    await state.set_state(EditPass.edit_pass)
    await state.update_data(edit=call.message.message_id)


@router.message(F.text, EditPass.edit_pass)
async def edit_pass_next(message: Message, state: FSMContext):
    answer = message.text
    await message.delete()
    data = await state.get_data()
    edit_pass_db(message=answer)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=data['edit'],
                                text=f'<b>🔒 Пароль</b>\n\n<tg-spoiler>{get_pass()}</tg-spoiler>', reply_markup=pass_edit())
    await state.clear()
