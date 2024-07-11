from datetime import datetime
from typing import List
from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    Text,
    DECIMAL,
    DateTime,
    Boolean,
    ForeignKey,
    JSON,
)
from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(String(length=64), nullable=True)
    name: Mapped[str] = mapped_column(String(length=64))
    date_reg: Mapped[str] = mapped_column(DateTime)
    last_idpk_form: Mapped[str] = mapped_column(Text, nullable=True)
    form_type: Mapped[str] = mapped_column(String(length=64), nullable=True)
    form_fields: Mapped[str] = mapped_column(Text, nullable=True)


class Subscriptions(Base):
    __tablename__ = "subscriptions"

    id_user: Mapped[int] = mapped_column(BigInteger)
    plan: Mapped[str] = mapped_column(String(length=64))
    date_start: Mapped[str] = mapped_column(DateTime, nullable=True)
    date_end: Mapped[str] = mapped_column(DateTime, nullable=True)


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


class BlackList(Base):
    __tablename__ = "blacklist"

    id_user: Mapped[int] = mapped_column(BigInteger)  # Идентификатор пользователя


class Value(Base):
    __tablename__ = "values"

    name: Mapped[str] = mapped_column(String(length=30))  # Название значения
    value_int: Mapped[int] = mapped_column(default=0)  # Значение целое
    value_str: Mapped[str] = mapped_column(
        String(length=4096), default="не установлено"
    )  # Значение строка


class SendedMessage(Base):
    __tablename__ = "sended_messages"

    id_message: Mapped[str] = mapped_column(String(length=64), unique=True)
    message: Mapped[str] = mapped_column(String(length=4096))


class PromoCode(Base):
    __tablename__ = "promo_codes"

    code: Mapped[str] = mapped_column(String(length=64), unique=True)
    discount: Mapped[int] = mapped_column(default=0)
    days_sub: Mapped[int] = mapped_column(default=0)
    num_enable_triggers: Mapped[int] = mapped_column(default=1)
    num_activated: Mapped[int] = mapped_column(default=0)