from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat

from tg_bot.data.config import ADMIN

# Команды для владельцев
owner_commands = {
    'start': '💼 Главное меню',
    'admin_menu': '👁 Меню админа'
}


# Установка команд
async def set_commands(bot: Bot):
    for admin in ADMIN:
        try:
            await bot.set_my_commands(
                [
                    BotCommand(command=command, description=description)
                    for command, description in owner_commands.items()
                ],
                scope=BotCommandScopeChat(chat_id=admin),
            )
        except:
            pass


# Удаление команд
async def remove_commands(bot: Bot):
    for admin in ADMIN:
        try:
            await bot.delete_my_commands(scope=BotCommandScopeChat(chat_id=admin))
        except:
            pass
