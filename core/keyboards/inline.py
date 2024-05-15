from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.utils.users_data import symptoms_in_group

select_symptoms_group = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='❌Общие симптомы',
            callback_data='group_common_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Боль',
            callback_data='group_pain_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Кровотечения и кровоизлияния',
            callback_data='group_blood_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Проблемы с кожей и слизистыми оболочками',
            callback_data='group_skin_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Проблемы с глазами',
            callback_data='group_eyes_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Проблемы с пищеварительной системой',
            callback_data='group_digestive_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Неврологические симптомы',
            callback_data='group_neurological_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Проблемы с мочевыделительной системой',
            callback_data='group_urinary_0'
        )
    ],
    [
        InlineKeyboardButton(
            text='❌Прочие симптомы',
            callback_data='group_other_0'
        )
    ]
]
)


def get_inline_keyboard(group):
    keyboard = InlineKeyboardBuilder()
    for symptom in symptoms_in_group[group]:
        keyboard.button(text=f'{symptoms_in_group[group][symptom][0]}{symptoms_in_group[group][symptom][1]}',
                        callback_data=f'symptom__{group}__{symptom}__{symptoms_in_group[group][symptom][2]}')

    keyboard.adjust(2)
    return keyboard.as_markup()
