from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tools import get_text_button


async def k_options_for_photo():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button('clear_selected'))
    builder.button(text=await get_text_button('confirm'))
    builder.button(text=await get_text_button('skip'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def k_confirm_del_form():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button('confirm_delete_form'))
    builder.button(text=await get_text_button('cancel'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
