from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from tools import get_text_button
from bot.keyboards import Response


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
    builder.button(text=await get_text_button("accept"), callback_data=f"response_accept:{idpk_form}")
    builder.button(text=await get_text_button("reject"), callback_data="response_reject")
    builder.adjust(1)
    return builder.as_markup()