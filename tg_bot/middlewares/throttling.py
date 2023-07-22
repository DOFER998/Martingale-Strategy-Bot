from typing import Callable, Awaitable, Any, Dict, Optional, MutableMapping

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User, Message, CallbackQuery
from cachetools import TTLCache

from tg_bot.data.config import RATE_LIMIT


class ThrottlingMiddleware(BaseMiddleware):

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache: MutableMapping[int, None] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            if user.id in self.cache:
                return await event.answer(text='⚠ Не так быстро!')

            self.cache[user.id] = None

        return await handler(event, data)


class ThrottlingCallbackMiddleware(BaseMiddleware):

    def __init__(self, rate_limit: float = RATE_LIMIT) -> None:
        self.cache: MutableMapping[int, None] = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Optional[Any]:
        user: Optional[User] = data.get("event_from_user", None)

        if user is not None:
            if user.id in self.cache:
                return await event.answer(text='⚠ Не так быстро!', show_alert=True)

            self.cache[user.id] = None

        return await handler(event, data)