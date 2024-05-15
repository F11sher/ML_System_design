from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Начало работы/доступные команды'
        ),
        BotCommand(
            command='description',
            description='Описание'
        ),
        BotCommand(
            command='diagnose',
            description='Начать диагностику'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
