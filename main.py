import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.chat_action import ChatActionMiddleware

from loguru import logger

from core.FSM.mainStates import MainStates
from core.handlers.admin_cmds import (get_admin, get_logs, get_full_drop, get_message_to_all_chats, get_message_text,
                                      send_message_to_all_chats)
from core.handlers.basic import (get_start, get_description, get_diagnose, get_symptoms_groups, get_symptoms,
                                 get_diagnose_result)
from core.handlers.callback import select_symptoms_group_call, select_symptoms_call
from core.settings import settings
from core.utils.commands import set_commands


@logger.catch
async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, text='Admin message: <b>Бот запущен!</b> ')
    logger.info(f'Bot start by Admin:{settings.bots.admin_id}')


@logger.catch
async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Admin message: <b>Бот отключен!</b>')
    logger.info(f'Bot stop by Admin:{settings.bots.admin_id}')


@logger.catch
async def start():
    logger.add(
        'logs/debug.log',
        format="{time} {level} {message}",
        level="DEBUG",
        rotation="1 week",
        compression="zip"
    )

    bot = Bot(token=settings.bots.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware.register(ChatActionMiddleware())

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.callback_query.register(select_symptoms_group_call, F.data.startswith('group_'))
    dp.callback_query.register(select_symptoms_call, F.data.startswith('symptom__'))

    dp.message.register(get_start, Command(commands=['start']), flags={'chat_action': 'typing'})
    dp.message.register(get_description, Command(commands=['description']), flags={'chat_action': 'typing'})
    dp.message.register(get_diagnose, Command(commands=['diagnose']), flags={'chat_action': 'typing'})

    dp.message.register(get_symptoms_groups,
                        MainStates.waitSymptomsGroup,
                        F.text == 'Группы симптомов выбраны!',
                        flags={'chat_action': 'typing'})
    dp.message.register(get_symptoms,
                        MainStates.waitSymptoms,
                        F.text == 'Подтвердить выбор',
                        flags={'chat_action': 'typing'})
    dp.message.register(get_diagnose_result,
                        MainStates.waitDiagnoseResult,
                        F.text == 'Готово',
                        flags={'chat_action': 'typing'})
    dp.message.register(get_admin,
                        Command(commands=['admin']),
                        flags={'chat_action': 'typing'}
                        )
    dp.message.register(get_logs,
                        Command(commands=['last_logs']),
                        flags={'chat_action': 'typing'})
    dp.message.register(get_full_drop,
                        Command(commands=['full_drop']),
                        flags={'chat_action': 'typing'})
    dp.message.register(get_message_to_all_chats,
                        Command(commands=['message_to_all_chats']),
                        flags={'chat_action': 'typing'})
    dp.message.register(get_message_text,
                        MainStates.waitChatID,
                        F.text,
                        flags={'chat_action': 'typing'})
    dp.message.register(send_message_to_all_chats,
                        MainStates.waitMessageForAll,
                        F.text,
                        flags={'chat_action': 'typing'})

    try:
        await dp.start_polling(bot)

    except Exception as ex:
        logger.error(f'Bot start error: {ex}')

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
