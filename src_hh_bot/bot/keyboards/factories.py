from aiogram.filters.callback_data import CallbackData


class Form(CallbackData, prefix="form"):
    field: int = 1

class Tag(CallbackData, prefix='t'):
    type: str = "tag"
    value: str