import os
import sys

from aiogram import Bot
from aiogram.types import Message
from loguru import logger
from asyncio import sleep
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from core.utils.users_data import user_data
from core.settings import settings
from core.FSM.mainStates import MainStates

list_of_chats = []


@logger.catch
async def get_admin(message: Message, bot: Bot):
    if message.from_user.id == settings.bots.admin_id:
        await bot.send_message(message.chat.id, '<b>Admin message:</b> Доступные команды администратора:\n\n'
                                                '/last_logs - получить файл с логами;\n'
                                                '/full_drop - экстренное отключение бота;\n'
                                                '/message_to_all_chats - отправить сообщение в список чатов;')


@logger.catch
async def get_logs(message: Message, bot: Bot):
    if message.from_user.id == settings.bots.admin_id:
        file = FSInputFile('./logs/debug.log')
        await bot.send_document(settings.bots.admin_id, file)

    else:
        await bot.send_message(message.chat.id, f'Данная команда доступна только <b>администратору</b> :(')


@logger.catch
async def get_full_drop(message: Message, bot: Bot):
    if message.from_user.id == settings.bots.admin_id:
        await bot.send_message(settings.bots.admin_id, '<b>Admin message:</b> <b>Начинаю экстренную остановку бота</b>')
        for key in user_data:
            await bot.send_message(key, '<b>Выполнена экстренная остановка бота администратором.</b>')

        await bot.send_message(settings.bots.admin_id, '<b>Admin message:</b> <b>Бот остановлен.</b>')
        file = FSInputFile('./logs/debug.log')
        await bot.send_document(settings.bots.admin_id, file)
        sys.exit()

    else:
        await bot.send_message(message.chat.id, f'Данная команда доступна только <b>администратору</b> :(')


@logger.catch
async def get_message_to_all_chats(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id == settings.bots.admin_id:
        logger.info('[Admin]: Администратор запустил массовую рассылку.')

        await bot.send_message(settings.bots.admin_id, '<b>Admin message:</b> Пришлите мне ответным сообщением список '
                                                       'чатов, в которые'
                                                       'необходимо отправить сообщение в формате:\n'
                                                       '<b>num_1\n'
                                                       'num_2\n'
                                                       '...\n'
                                                       'num_n</b>')
        await state.set_state(MainStates.waitChatID)
        logger.info('[Admin]: Ожидаю список чатов для рассылки...')

    else:
        await bot.send_message(message.chat.id, f'Данная команда доступна только <b>администратору</b> :(')


@logger.catch
async def get_message_text(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id == settings.bots.admin_id:
        global list_of_chats
        list_of_chats = message.text.split('\n')
        logger.info(f'[Admin]: Получил список чатов:\n'
                    f'{list_of_chats}')

        await bot.send_message(settings.bots.admin_id, '<b>Admin message:</b> Теперь пришлите мне ответным сообщением '
                                                       'текст для рассылки:')
        await state.set_state(MainStates.waitMessageForAll)
        logger.info('[Admin]: Ожидаю текст сообщения для рассылки...')

    else:
        await bot.send_message(message.chat.id, f'Данная команда доступна только <b>администратору</b> :(')


@logger.catch
async def send_message_to_all_chats(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id == settings.bots.admin_id:
        global list_of_chats

        logger.info('[Admin]: Начинаю рассылку...')
        for uid in list_of_chats:
            await bot.send_message(uid, message.text)
            logger.info(f'[Admin]: Отправил рассылку в чат: {uid}')

        list_of_chats = []
        await state.clear()
        await bot.send_message(settings.bots.admin_id, '<b>Admin message:</b> Закончил рассылку во все чаты.')
        logger.info('[Admin]: Закончил рассылку.')

    else:
        await bot.send_message(message.chat.id, f'Данная команда доступна только <b>администратору</b> :(')
