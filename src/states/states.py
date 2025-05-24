from aiogram.fsm.state import State, StatesGroup
class RegistrationStates(StatesGroup):
    waiting_for_first_name = State()
    waiting_for_last_name = State()
class ScoreStates(StatesGroup):
    waiting_for_subject = State()
    waiting_for_score = State()