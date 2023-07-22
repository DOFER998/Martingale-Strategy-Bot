from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from tg_bot.data.database import get_password, get_messages
from tg_bot.keyboards.user.replay import start_strategy_user
from tg_bot.middlewares.update_db import AddOrUpdateCallbackMiddleware, AddOrUpdateMiddleware
from tg_bot.misc.states import Password

router = Router(name="User main router")
router.message.filter(F.chat.type == "private")
router.message.middleware(AddOrUpdateMiddleware())
router.callback_query.outer_middleware(AddOrUpdateCallbackMiddleware())


@router.message(Command(commands=['start']))
async def cmd_user_start(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(text=get_messages()['1'].format(user=message.from_user.first_name))
    await state.set_state(Password.password)


@router.message(F.text, Password.password)
async def input_password(message: Message, state: FSMContext):
    if message.text != get_password():
        await message.answer(text='❌ Ошибка, неверный пароль, попробуйте еще раз!')
        return

    await message.answer(text=get_messages()['2'].format(user=message.from_user.first_name),
                         reply_markup=start_strategy_user())
    await state.clear()
