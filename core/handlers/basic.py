from copy import deepcopy

from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from loguru import logger

from core.settings import settings
from core.FSM.mainStates import MainStates
from core.keyboards.inline import select_symptoms_group, get_inline_keyboard
from core.keyboards.reply import get_reply_keyboard
from core.utils.users_data import buttons_group_data, symptoms_in_group, result_symptoms, user_data
from core.utils.models import get_predict
from core.utils.texts import symptoms_group, symptoms_description


@logger.catch
async def get_start(message: Message, bot: Bot):
    with open('chat_id_list.txt', 'r+') as file:
        chat_id = message.chat.id

        if message.chat.title is None:
            title = message.from_user.first_name

        else:
            title = message.chat.title

        chat_id_list = file.readlines()
        if f'{chat_id} - {title}\n' not in chat_id_list:
            file.write(f'{chat_id} - {title}\n')
            logger.info(f'Новый пользователь подключился к боту! Chat_id: {chat_id}; Title: {title}')
            await bot.send_message(settings.bots.admin_id, f'<b>Admin message: Новый пользователь подключился к боту:\n'
                                                           f'Chat_id: {chat_id}\n'
                                                           f'Title: {title}</b>')

    await bot.send_message(message.chat.id, f'<b>Доступные команды:\n'
                                            f'/discription - Описание данного бота\n'
                                            f'/diagnose - Начать диагностику болезни\n\n'
                                            f'Аккаунты технической поддержки:\n'
                                            f'<a href="https://t.me/F1sher_r">@F1sher_r</a>\n'
                                            f'<a href="https://t.me/vasiliy_goloskov">@vasiliy_goloskov</a></b>')


@logger.catch
async def get_description(message: Message, bot: Bot):
    logger.info(f'[{message.chat.id}]: Запрошено описание бота.')
    await bot.send_message(message.chat.id, '<b>*Здесь будет описание работы бота*</b>')


@logger.catch
async def get_diagnose(message: Message, bot: Bot, state: FSMContext):
    logger.info(f'[{message.chat.id}]: Запущена диагностика')

    if message.chat.id not in user_data:
        user_data[message.chat.id] = [deepcopy(buttons_group_data),
                                      deepcopy(symptoms_in_group),
                                      deepcopy(result_symptoms)]

    await bot.send_message(message.chat.id,
                           'Вы запустили диагностику!\n'
                           'Выберите группы ваших симптомов:\n'
                           f'{symptoms_group}',
                           reply_markup=select_symptoms_group)

    await message.answer('Для подтверждения своего выбора нажмите кнопку на "Группы симптомов выбраны!"',
                         reply_markup=get_reply_keyboard('Группы симптомов выбраны!'))

    logger.info(f'[{message.chat.id}]: Ожидаю выбора групп симптомов...')

    await state.set_state(MainStates.waitSymptomsGroup)


@logger.catch
async def get_symptoms_groups(message: Message, bot: Bot, state: FSMContext):
    logger.info(f'[{message.chat.id}]: Получил список симптомов!')

    selected_groups = ''
    counter = 1
    for group in user_data[message.chat.id][0]:
        if user_data[message.chat.id][0][group][2] == 1:
            selected_groups += f'{counter}. {user_data[message.chat.id][0][group][1]}\n'
            counter += 1

    await bot.send_message(message.chat.id,
                           f'Были выбраны группы:\n\n'
                           f'<i>{selected_groups}</i>\n'
                           f'После <b>подтверждения выбора</b> рассмотрим каждую отдельно.',
                           reply_markup=get_reply_keyboard('Подтвердить выбор'))

    logger.info(f'[{message.chat.id}]: Ожидаю подтверждения выбора...')
    await state.set_state(MainStates.waitSymptoms)


@logger.catch
async def get_symptoms(message: Message, bot: Bot, state: FSMContext):
    logger.info(f'[{message.chat.id}]: Выбор подтвержден!')
    await bot.send_message(message.chat.id,
                           'Выбор подтвержден!\n'
                           'Теперь пройдемся по каждой группе отдельно:',
                           reply_markup=get_reply_keyboard('Готово'))

    for group in user_data[message.chat.id][0]:
        if user_data[message.chat.id][0][group][2] == 1:
            logger.info(f'[{message.chat.id}]: Ожидаю симптомы из группы '
                        f'"{user_data[message.chat.id][0][group][1]}"...')

            await bot.send_message(message.chat.id,
                                   f'Выберите симптомы из группы "{user_data[message.chat.id][0][group][1]}":',
                                   reply_markup=get_inline_keyboard(group))

    await state.set_state(MainStates.waitDiagnoseResult)


@logger.catch
async def get_diagnose_result(message: Message, bot: Bot, state: FSMContext):
    logger.info(f'[{message.chat.id}]: Получил список симптомов от пользователя!')
    waiting_message = await bot.send_message(message.chat.id,
                                             f'Список симптомов получен!\n'
                                             f'Начинаю обработку...',
                                             reply_markup=ReplyKeyboardRemove())

    for group in user_data[message.chat.id][0]:
        if user_data[message.chat.id][0][group][2] == 1:
            for symptom in user_data[message.chat.id][1][group]:
                user_data[message.chat.id][2][symptom] = user_data[message.chat.id][1][group][symptom][2]
    logger.info(f'[{message.chat.id}]: Данные записаны, начинаю обработку...')

    result = await get_predict(user_data[message.chat.id][2])
    logger.info(f'[{message.chat.id}]: Результат получен!')

    await waiting_message.delete()
    await bot.send_message(message.chat.id, f'Обработка завершена!\n'
                                            f'Ваш результат: <b>{result[1]}</b>\n\n'
                                            f'{symptoms_description[result[0]]}')

    user_data[f'{message.chat.id}__{message.message_id}_{result[0]}'] = user_data[message.chat.id][2]
    logger.info(f'[{message.chat.id}]: Результат сохранен')

    with open('users_data.txt', 'r+', encoding='utf-8') as save_data:
        for data in user_data:
            if f'{data}: {user_data[data]}\n\n' not in save_data:
                save_data.write(f'{data}: {user_data[data]}\n\n')
        logger.info('[Admin]: Данные пользователей обновлены')
        await bot.send_message(settings.bots.admin_id, 'Admin message: <b>Данные пользователей обновлены!</b>')

    del user_data[message.chat.id]
    logger.info(f'[{message.chat.id}]: Данные пользователя очищены')

    await state.clear()
    logger.info(f'[{message.chat.id}]: Обработка завершена')
