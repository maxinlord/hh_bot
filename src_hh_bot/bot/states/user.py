from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    main = State()