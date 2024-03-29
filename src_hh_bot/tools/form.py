from sqlalchemy import select
from db import Text, Button, Value
from init_db import _sessionmaker_for_func
from tools import get_text_message


async def form_not_complete(data: dict, field_to_skip: list, type_form: str = 'one') -> list:
    """
    Функция для проверки заполненности формы
    :param data: словарь данных из формы
    :return: список незаполненных полей
    """
    not_complete_fields = []
    not_set = await get_text_message("not_set")
    for field, value in data.items():
        if field in field_to_skip:
            continue
        if value == not_set:
            not_complete_fields.append(await get_text_message(f'form_{type_form}_{field}_not_complete'))
    return not_complete_fields