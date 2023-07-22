from aiogram.fsm.state import StatesGroup, State


class Password(StatesGroup):
    password = State()


class Bid(StatesGroup):
    bid = State()


class EditMessage(StatesGroup):
    edit_message = State()


class EditButton(StatesGroup):
    edit_button = State()


class EditPass(StatesGroup):
    edit_pass = State()
