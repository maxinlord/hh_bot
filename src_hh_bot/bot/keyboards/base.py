from aiogram.utils.keyboard import InlineKeyboardBuilder
from tools import get_text_button


async def k_back():
    builder = InlineKeyboardBuilder()
    builder.button(text=await get_text_button('back'), callback_data='back')
    return builder.as_markup()

async def k_cancel():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button('cancel'))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)