import re

from cache import button_cache, text_cache
from db import Button, Text, Value
from init_db import _sessionmaker_for_func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_text_message(name: str, **kw) -> str:
    async with _sessionmaker_for_func() as session:
        if name in text_cache:
            text_obj = text_cache[name]
        else:
            text_obj = await _get_or_create_text(session, name)
            text_cache[name] = text_obj

        debug_key = "debug_key_text"
        if debug_key in text_cache:
            debug_text = text_cache[debug_key]
        else:
            debug_text = await session.scalar(
                select(Value.value_int).where(Value.name == "DEBUG_TEXT")
            )
            text_cache[debug_key] = debug_text
        formatted_text = await _format_text(
            text_obj=text_obj,
            debug_text=debug_text,
            kw=kw,
        )
        await session.commit()
        return formatted_text


async def _get_or_create_text(session: AsyncSession, name):
    text_obj = await session.scalar(select(Text).where(Text.name == name))
    if not text_obj:
        text_obj = Text(name=name)
        session.add(text_obj)
        await session.commit()
    return text_obj


async def _get_or_create_button(session, name):
    bttn_obj: Text = await session.scalar(select(Button).where(Button.name == name))
    if not bttn_obj:
        bttn_obj = Button(name=name)
        session.add(bttn_obj)
    return bttn_obj


async def _format_text(text_obj: Text, kw: dict, debug_text: int = 0):
    prefix = f"[{text_obj.name}]\n" if debug_text else ""
    if not kw:
        return f"{prefix}{text_obj.text}"
    return f"{prefix}{text_obj.text.format(**kw)}"


async def _format_button(bttn_obj: Text, kw: dict, debug_button: int = 0):
    prefix = f"[{bttn_obj.name}]|" if debug_button else ""
    if not kw:
        return f"{prefix}{bttn_obj.text}"
    return f"{prefix}{bttn_obj.text.format(**kw)}"


async def get_text_button(name: str, **kw) -> str:
    async with _sessionmaker_for_func() as session:
        if name in button_cache:
            bttn_obj = button_cache[name]
        else:
            bttn_obj = await _get_or_create_button(session, name)
            button_cache[name] = bttn_obj

        debug_key = "debug_key_button"
        if debug_key in button_cache:
            debug_button = button_cache[debug_key]
        else:
            debug_button = await session.scalar(
                select(Value.value_int).where(Value.name == "DEBUG_BUTTON")
            )
            button_cache[debug_key] = debug_button
        formatted_bttn = await _format_button(
            bttn_obj=bttn_obj,
            kw=kw,
            debug_button=debug_button,
        )
        await session.commit()
        return formatted_bttn


def mention_html(id_user: int, name: str) -> str:
    return f'<a href="tg://user?id={id_user}">{name}</a>'


def mention_html_by_username(username: str, name: str) -> str:
    return f'<a href="http://t.me/{username}">{name}</a>' if username else name


def validate_input(input_str):
    # Регулярное выражение для проверки формата
    pattern = r"^\d{1,9}-\d{1,9}р?$"

    # Проверка соответствия регулярному выражению
    return bool(re.match(pattern, input_str))
