import math
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from tg_bot.data.database import get_messages, edit_info_user, get_info_user, get_buttons
from tg_bot.keyboards.user.inline import choice_user_stake
from tg_bot.middlewares.update_db import AddOrUpdateCallbackMiddleware, AddOrUpdateMiddleware
from tg_bot.misc.states import Bid
from tg_bot.utils.number import is_number
from tg_bot.utils.random_coefficient import random_number

router = Router(name="User strategy router")
router.message.filter(F.chat.type == "private")
router.message.middleware(AddOrUpdateMiddleware())
router.callback_query.outer_middleware(AddOrUpdateCallbackMiddleware())


@router.message(F.text == get_buttons()['4'])
async def start_strategy(message: Message, state: FSMContext):
    await message.delete()
    await message.answer(text=get_messages()['3'].format(user=message.from_user.first_name),
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(Bid.bid)


@router.callback_query(F.data.startswith('winning:'))
async def winning(call: CallbackQuery):
    int = random_number()
    info = get_info_user(user_id=call.message.chat.id)
    await call.message.answer(
        text=get_messages()['4'].format(user=call.message.chat.first_name, coeff=float(int),
                                        int=math.trunc(info['info']),
                                        final=math.trunc(float(int) * float(info["info"]))).replace(',', '.'),
        reply_markup=choice_user_stake(amount=info['info'], coeff=float(int)))
    await call.answer()


@router.callback_query(F.data.startswith('losing:'))
async def losing(call: CallbackQuery):
    data = call.data.split(":")
    await call.message.answer(text=get_messages()['5'].format(user=call.message.chat.first_name, coeff=float(data[2]),
                                                              int=math.trunc(float(data[1]) * 1.5),
                                                              final=math.trunc(
                                                                  float(data[2]) * float(data[1]))).replace(',', '.'),
                              reply_markup=choice_user_stake(amount=float(data[1]) * 1.5, coeff=data[2]))
    await call.answer()


@router.callback_query(F.data == 'stop')
async def losing(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text=get_messages()['3'].format(user=call.message.chat.first_name))
    await state.set_state(Bid.bid)
    await call.answer()


@router.message(F.text, Bid.bid)
async def random_coefficient(message: Message, state: FSMContext):
    if not is_number(str=message.text):
        await message.answer(text=get_messages()['9'])
        return
    elif int(message.text) < 1020:
        await message.answer(text=get_messages()['10'])
        return
    elif int(message.text) > 502000:
        await message.answer(text=get_messages()['11'])
        return

    number = random_number()
    await message.answer(
        text=get_messages()['6'].format(user=message.from_user.first_name, coeff=float(number),
                                        int=math.trunc(float(message.text)),
                                        final=math.trunc(float(number) * float(message.text))).replace(',', '.'),
        reply_markup=choice_user_stake(amount=message.text, coeff=number))
    edit_info_user(user_id=message.from_user.id, info=float(message.text))
    await state.clear()
