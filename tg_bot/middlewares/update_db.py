from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from tg_bot.data.database import add_user


class AddOrUpdateMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        add_user(
            user_id=event.from_user.id,
            user_name=event.from_user.username,
            nick_name=event.from_user.first_name
        )

        return await handler(event, data)


class AddOrUpdateCallbackMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        add_user(
            user_id=event.message.chat.id,
            user_name=event.message.chat.username,
            nick_name=event.message.chat.first_name
        )

        return await handler(event, data)
