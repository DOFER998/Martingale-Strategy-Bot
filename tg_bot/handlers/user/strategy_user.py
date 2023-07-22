from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tg_bot.data.database import get_messages
from tg_bot.keyboards.user.inline import choice_user_stake
from tg_bot.middlewares.update_db import AddOrUpdateCallbackMiddleware, AddOrUpdateMiddleware
from tg_bot.misc.states import Bid
from tg_bot.utils.number import is_number
from tg_bot.utils.random_coefficient import random_number

router = Router(name="User strategy router")
router.message.filter(F.chat.type == "private")
router.message.middleware(AddOrUpdateMiddleware())
router.callback_query.outer_middleware(AddOrUpdateCallbackMiddleware())


@router.message(F.text == '💰 Начать стратегию')
async def start_strategy(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(text=get_messages()['3'].format(user=message.from_user.first_name),
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Bid.bid)


@router.callback_query(F.data.startswith('winning:'))
async def winning(call: CallbackQuery):
    data = call.data.split(":")
    int = random_number()
    await call.message.answer(
        text=get_messages()['4'].format(user=call.message.chat.first_name, coeff=float(int), int=float(data[1])),
        reply_markup=choice_user_stake(amount=data[1], coeff=int))
    await call.answer()


@router.callback_query(F.data.startswith('losing:'))
async def losing(call: CallbackQuery):
    data = call.data.split(":")
    await call.message.answer(
        text=get_messages()['5'].format(user=call.message.chat.first_name, coeff=float(data[2]),
                                        int=float(data[1]) * 2),
        reply_markup=choice_user_stake(amount=int(data[1]) * 2, coeff=data[2]))
    await call.answer()


@router.callback_query(F.data == 'stop')
async def losing(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text=get_messages()['3'].format(user=call.message.chat.first_name))
    await state.set_state(Bid.bid)
    await call.answer()


@router.message(F.text, Bid.bid)
async def random_coefficient(message: Message, state: FSMContext):
    if not is_number(str=message.text):
        await message.answer(text='❌ Ошибка, нужно ввести число!')
        return

    int = random_number()
    await message.answer(
        text=get_messages()['6'].format(user=message.from_user.first_name, coeff=float(int), int=float(message.text)),
        reply_markup=choice_user_stake(amount=message.text, coeff=int))
    await state.clear()
