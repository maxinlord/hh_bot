import csv
import json
import random
import string

from db import BlackList, SendedMessage, User
from init_db import _sessionmaker_for_func
from sqlalchemy import and_, select

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
        user.form_fields = None
        user.form_type = None
        await session.commit()


async def get_forms_idpk_by_tag(
    tag: str,
    form_type: str,
    last_form_idpk: int | str,
    city: str = "",
) -> list:
    async with _sessionmaker_for_func() as session:
        blacklist = await session.scalars(select(BlackList.id_user))
        forms = await session.scalars(
            select(User.idpk).where(
                and_(
                    User.form_fields.contains(city),
                    User.form_fields.contains(tag),
                    User.form_type == form_type,
                    User.id_user.not_in(blacklist),
                )
            )
        )
        forms = list(forms)
        if not last_form_idpk:
            return forms
        if not forms:
            return []
        if isinstance(last_form_idpk, int):
            _, forms_idpk = split_list_index(forms, last_form_idpk)
        else:
            last_form_idpk: dict = json.loads(last_form_idpk)
            _, forms_idpk = split_list_index(forms, last_form_idpk.get(tag, 0))
        return forms_idpk


async def get_forms_idpk(
    form_type: str, last_form_idpk: int | str, city: str = ""
) -> list:
    async with _sessionmaker_for_func() as session:
        blacklist = set(await session.scalars(select(BlackList.id_user)))
        forms = await session.scalars(
            select(User.idpk).where(
                and_(
                    User.form_type == form_type,
                    User.id_user.not_in(blacklist),
                    User.form_fields.contains(city),
                )
            )
        )
        forms = list(forms)
        if not forms or not last_form_idpk:
            return forms

        if isinstance(last_form_idpk, str):
            last_form_idpk = json.loads(last_form_idpk).get("__all", 0)

        _, forms_idpk = split_list_index(forms, last_form_idpk)
        return forms_idpk


async def get_city(form_fields: str) -> str:
    form_fields = json.loads(form_fields)
    city = form_fields.get("city", "")
    return city


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
        return [], list_
    if len(list_) == 1:
        return [], []
    index = list_.index(element)
    first_part = list_[:index]
    second_part = list_[index + 1 :]
    return first_part, second_part


form_type_inverter = {"one": "two", "two": "one", "three": "four", "four": "three"}


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


async def to_dict_form_fields(form_fields: str) -> dict:
    form_fields = json.loads(form_fields)
    return form_fields


def load_cities(filename):
    cities = set()
    with open(filename, "r", encoding="utf-8") as file:
        for row in csv.reader(file):
            cities.add(row[6].strip())
            if row[1] == "г":
                cities.add(row[2].strip())
    return cities


# Загрузка списка городов из файла
cities = load_cities("cities.csv")


async def is_city_exist(city_name: str):
    return city_name.strip().capitalize() in cities
