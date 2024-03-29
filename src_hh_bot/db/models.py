from datetime import datetime
from typing import List
from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    DECIMAL,
    DateTime,
    Boolean,
    ForeignKey,
)
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(length=64))


class Text(Base):
    __tablename__ = "texts"

    name: Mapped[str] = mapped_column(String(length=100))  # Название текста
    text: Mapped[str] = mapped_column(
        String(length=4096), default="текст не задан"
    )  # Текст


class Button(Base):
    __tablename__ = "buttons"

    name: Mapped[str] = mapped_column(String(length=30))  # Название кнопки
    text: Mapped[str] = mapped_column(
        String(length=64), default="кнопка"
    )  # Текст кнопки


class Photo(Base):
    __tablename__ = "photos"

    name: Mapped[str] = mapped_column(String(length=30))  # Название фото
    photo_id: Mapped[str] = mapped_column(String(length=100))  # Ссылка на фото


class BlackList(Base):
    __tablename__ = "blacklist"

    id_user: Mapped[int] = mapped_column(BigInteger)  # Идентификатор пользователя
    date_unban: Mapped[str] = mapped_column(DateTime)  # Дата разбана


class Value(Base):
    __tablename__ = "values"

    name: Mapped[str] = mapped_column(String(length=30))  # Название значения
    value_int: Mapped[int] = mapped_column(default=0)  # Значение целое
    value_str: Mapped[str] = mapped_column(String(length=4096), default="не установлено")  # Значение строка
