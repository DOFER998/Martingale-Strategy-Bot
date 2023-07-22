from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdmin(BaseFilter):
    def __init__(self, user: Union[list]):
        self.user = user

    async def __call__(self, message: Message) -> bool:
        return str(message.from_user.id) in self.user
