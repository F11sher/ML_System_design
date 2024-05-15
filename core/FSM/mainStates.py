from aiogram.fsm.state import State, StatesGroup


class MainStates(StatesGroup):
    waitMessageForAll = State()
    waitChatID = State()
    waitSymptomsGroup = State()
    waitSymptoms = State()
    waitDiagnoseResult = State()
