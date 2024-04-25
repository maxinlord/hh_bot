from sqlalchemy import select, and_
from db import User, SendedMessage, BlackList
from init_db import _sessionmaker_for_func
from tools import get_text_message
import random
import string
import json


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


async def get_idpk_forms_by_tag(
    tag: str, form_type: str, last_idpk_form: int | str
) -> list:
    async with _sessionmaker_for_func() as session:
        blacklist = await session.scalars(select(BlackList.id_user))
        blacklist = blacklist.all()
        forms = await session.scalars(
            select([User.idpk, User.id_user]).where(
                and_(User.field_4 == tag, User.form_type == form_type)
            )
        )
        forms = forms.all()
        forms = [form[0] for form in forms if form[1] not in blacklist]
        if not last_idpk_form:
            return forms
        if not forms:
            return []
        match isinstance(last_idpk_form, int):
            case True:
                forms = split_list_index(forms, last_idpk_form)[1]
            case False:
                last_idpk_form: dict = json.loads(last_idpk_form)
                forms = split_list_index(forms, last_idpk_form.get(tag, 0))[1]
        return forms


async def get_idpk_forms(form_type: str, last_idpk_form: int | str) -> list:
    async with _sessionmaker_for_func() as session:
        blacklist = await session.scalars(select(BlackList.id_user))
        blacklist = blacklist.all()
        forms = await session.scalars(
            select([User.idpk, User.id_user]).where(User.form_type == form_type)
        )
        forms = forms.all()
        forms = [form[0] for form in forms if form[1] not in blacklist]
        if not last_idpk_form:
            return forms
        if not forms:
            return []
        match isinstance(last_idpk_form, int):
            case True:
                forms = split_list_index(forms, last_idpk_form)[1]
            case False:
                last_idpk_form: dict = json.loads(last_idpk_form)
                forms = split_list_index(forms, last_idpk_form.get("__all", 0))[1]
        return forms


def split_list_index(list_: list, element: any):
    """
    Функция для разделения списка на две части по индексу элемента
    :param list_: список
    :param element: элемент списка
    :return: две части списка, без указанного элемента
    """
    if element == 0:
        return [], list_
    if element > list_[-1]:
        return [], []
    if element not in list_:
        raise ValueError("Элемент не найден в списке")
    if len(list_) == 1:
        return [], []
    index = list_.index(element)
    first_part = list_[:index]
    second_part = list_[index + 1 :]
    return first_part, second_part


form_type_inverter = {
    "one": "two",
    "two": "one",
}


def gen_id(len_: int) -> str:

    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    id_ = "".join(random.choice(letters) for _ in range(len_))
    return id_


async def save_message(mess: str) -> str:
    async with _sessionmaker_for_func() as session:
        id_message = gen_id(10)
        message = SendedMessage(id_message=id_message, message=mess)
        session.add(message)
        await session.commit()
    return id_message


async def delete_message(id_message: str) -> None:
    async with _sessionmaker_for_func() as session:
        message = await session.scalar(
            select(SendedMessage).where(SendedMessage.id_message == id_message)
        )
        await session.delete(message)
        await session.commit()
