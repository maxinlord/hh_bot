from aiogram.fsm.state import State, StatesGroup


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


class FormThreeState(StatesGroup):
    main = State()
    enter_city = State()
    edit_enter_city = State()
    field_1 = State()
    field_2 = State()
    field_3 = State()
    field_4 = State()
    field_5 = State()
    field_6 = State()


class FormFourState(StatesGroup):
    main = State()
    enter_city = State()
    edit_enter_city = State()
    field_1 = State()
    field_2 = State()
    field_3 = State()
    field_4 = State()
    field_5 = State()
    field_6 = State()


class ViewForm(StatesGroup):
    main = State()
    chose_tag = State()
    response = State()
    report = State()
