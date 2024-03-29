from aiogram.utils.keyboard import InlineKeyboardBuilder
from tools import get_text_button
from bot.keyboards import Form

async def k_form_fields(form_type: str = 'one'):
    builder = InlineKeyboardBuilder()
    builder.button(text=await get_text_button(f'form_{form_type}_field_1'), callback_data=Form())
    builder.button(text=await get_text_button(f'form_{form_type}_field_2'), callback_data=Form(field=2))
    builder.button(text=await get_text_button(f'form_{form_type}_field_3'), callback_data=Form(field=3))
    builder.button(text=await get_text_button(f'form_{form_type}_field_4'), callback_data=Form(field=4))
    builder.button(text=await get_text_button(f'form_{form_type}_field_5'), callback_data=Form(field=5))
    builder.button(text=await get_text_button('end_reg'), callback_data=f'end_reg_{form_type}')
    builder.adjust(1, 2, 2, 1)
    return builder.as_markup()