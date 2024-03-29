from aiogram.utils.keyboard import InlineKeyboardBuilder
from tools import get_text_button


async def k_types_of_reg():
    builder = InlineKeyboardBuilder()
    builder.button(text=await get_text_button('reg_one'), callback_data='reg_one')
    builder.button(text=await get_text_button('reg_two'), callback_data='reg_two')
    builder.adjust(1)
    return builder.as_markup()
