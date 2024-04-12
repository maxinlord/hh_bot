from aiogram.fsm.state import StatesGroup, State


class FormOneState(StatesGroup):
    main = State()
    field_1 = State()
    field_2 = State()
    field_3 = State()
    field_4 = State()
    field_5 = State()

class FormTwoState(StatesGroup):
    main = State()
    field_1 = State()
    field_2 = State()
    field_3 = State()
    field_4 = State()
    field_5 = State()

class ViewForm(StatesGroup):
    main = State()
    chose_tag = State()
    response = State()
    report = State()