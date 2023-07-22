import asyncio
import logging

from aiogram import Bot, Dispatcher

from tg_bot.data.loader import bot, dp
from tg_bot.handlers import get_handlers_router
from tg_bot.middlewares.throttling import ThrottlingMiddleware, ThrottlingCallbackMiddleware
from tg_bot.misc.commands import set_commands, remove_commands


async def on_startup(dispatcher: Dispatcher, bot: bot):
    dispatcher.include_router(get_handlers_router())
    dispatcher.message.middleware(ThrottlingMiddleware())
    dispatcher.callback_query.outer_middleware(ThrottlingCallbackMiddleware())
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    logging.error('Bot started!')


async def on_shutdown(dispatcher: Dispatcher, bot: Bot):
    logging.warning('Stopping bot...')
    await remove_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.fsm.storage.close()
    await bot.session.close()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):

        logging.error("Bot stopped!")
