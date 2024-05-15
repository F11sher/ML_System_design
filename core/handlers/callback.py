from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery
from loguru import logger

from core.utils.users_data import user_data


async def select_symptoms_group_call(call: CallbackQuery):
    callback = call.data.split('_')
    group = callback[1]
    state = int(callback[2])
    if state == 0:
        new_state = 1
        new_check = '✅'
        logger.info(f'[{call.message.chat.id}]: Выбрана группа "{user_data[call.message.chat.id][0][group][1]}"')

    else:
        new_state = 0
        new_check = '❌'
        logger.info(f'[{call.message.chat.id}]: Выбор группы "{user_data[call.message.chat.id][0][group][1]}" отменен')

    user_data[call.message.chat.id][0][group][0] = new_check
    user_data[call.message.chat.id][0][group][2] = new_state

    new_keyboard = InlineKeyboardBuilder()
    for symptom in user_data[call.message.chat.id][0]:
        new_keyboard.button(text=f'{user_data[call.message.chat.id][0][symptom][0]}'
                                 f'{user_data[call.message.chat.id][0][symptom][1]}',
                            callback_data=f'group_{symptom}_{user_data[call.message.chat.id][0][symptom][2]}')

    new_keyboard.adjust(1)

    await call.message.edit_reply_markup(reply_markup=new_keyboard.as_markup())
    await call.answer()


async def select_symptoms_call(call: CallbackQuery):
    callback = call.data.split('__')
    group = callback[1]
    symptom = callback[2]
    state = int(callback[3])
    if state == 0:
        new_state = 1
        new_check = '✅'
        logger.info(f'[{call.message.chat.id}]: Выбран симптом "{user_data[call.message.chat.id][1][group][symptom][1]}"'
                    f' из группы "{user_data[call.message.chat.id][0][group][1]}"')

    else:
        new_state = 0
        new_check = '❌'
        logger.info(f'[{call.message.chat.id}]: Выбор симптома "{user_data[call.message.chat.id][1][group][symptom][1]}" '
                    f' из группы "{user_data[call.message.chat.id][0][group][1]}" отменен')

    user_data[call.message.chat.id][1][group][symptom][0] = new_check
    user_data[call.message.chat.id][1][group][symptom][2] = new_state

    new_keyboard = InlineKeyboardBuilder()
    for symptom in user_data[call.message.chat.id][1][group]:
        new_keyboard.button(text=f'{user_data[call.message.chat.id][1][group][symptom][0]}'
                                 f'{user_data[call.message.chat.id][1][group][symptom][1]}',
                            callback_data=f'symptom__{group}__{symptom}__'
                                          f'{user_data[call.message.chat.id][1][group][symptom][2]}')

    new_keyboard.adjust(2)

    await call.message.edit_reply_markup(reply_markup=new_keyboard.as_markup())
    await call.answer()
