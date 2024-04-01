from db import User
from init_db import _sessionmaker_for_func
from tools import get_text_message


async def form_not_complete(
    data: dict, field_to_skip: list, type_form: str = "one"
) -> list:
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
            not_complete_fields.append(
                await get_text_message(f"form_{type_form}_{field}_not_complete")
            )
    return not_complete_fields


async def delete_form(idpk_user: int) -> None:
    async with _sessionmaker_for_func() as session:
        user = await session.get(User, idpk_user)
        user.field_1 = None
        user.field_2 = None
        user.field_3 = None
        user.field_4 = None
        user.field_5 = None
        user.form_type = None
        user.photos_id = None
        await session.commit()
