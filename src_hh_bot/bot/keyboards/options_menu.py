from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from bot.keyboards import Ban, Response
from tools import get_text_button


async def k_options_for_photo():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button("clear_selected"))
    builder.button(text=await get_text_button("confirm"))
    builder.button(text=await get_text_button("skip"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def k_confirm_del_form():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button("confirm_delete_form"))
    builder.button(text=await get_text_button("cancel"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def k_view_response(idpk_form: int, id_message: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=await get_text_button("view_respond"),
        callback_data=Response(id_message=id_message, idpk_form=idpk_form),
    )
    builder.adjust(1)
    return builder.as_markup()


async def k_accept_or_reject(idpk_form: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=await get_text_button("accept"),
        callback_data=f"response_accept:{idpk_form}",
    )
    builder.button(
        text=await get_text_button("reject"), callback_data="response_reject"
    )
    builder.adjust(1)
    return builder.as_markup()


async def k_ban(idpk_user: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text=await get_text_button("ban"), callback_data=Ban(idpk_user=idpk_user)
    )
    builder.adjust(1)
    return builder.as_markup()


async def k_subscribe():
    builder = InlineKeyboardBuilder()
    builder.button(text=await get_text_button("subscribe"), callback_data="sub")
    builder.adjust(1)
    return builder.as_markup()


async def k_skip():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button("skip"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
