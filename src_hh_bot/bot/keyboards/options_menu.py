from aiogram.utils.keyboard import ReplyKeyboardBuilder
from tools import get_text_button


async def k_options_for_photo():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button('clear_selected'))
    builder.button(text=await get_text_button('back'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)
