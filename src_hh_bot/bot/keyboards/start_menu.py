from aiogram.utils.keyboard import InlineKeyboardBuilder
from tools import get_text_button


async def k_start_menu():
    builder = InlineKeyboardBuilder()
    builder.button(text=await get_text_button('registration'), callback_data='select_reg')
    builder.button(text=await get_text_button('conditions_and_recommendations'), callback_data='pre_reg_info')
    builder.adjust(1)
    return builder.as_markup()
