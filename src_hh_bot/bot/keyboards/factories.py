from aiogram.filters.callback_data import CallbackData


class Form(CallbackData, prefix="form"):
    field: int = 1

class Tag(CallbackData, prefix='t'):
    type: str = "tag"
    value: str

class Response(CallbackData, prefix='r'):
    type: str = "response"
    idpk_form: int
    id_message: str

class Ban(CallbackData, prefix='b'):
    type: str = "ban"
    idpk_user: int