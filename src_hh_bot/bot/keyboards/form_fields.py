from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from tools import get_text_button
from bot.keyboards import Form


async def k_form_fields(
    form_type: str = "one",
    amount_fields: int = 5,
    adjust: list = None,
    change_city: bool = False,
):
    if not adjust:
        adjust = [1, 2, 2]
    builder = InlineKeyboardBuilder()
    for i in range(1, amount_fields + 1):
        builder.button(
            text=await get_text_button(f"form_{form_type}_field_{i}"),
            callback_data=Form(field=i),
        )
    tail = [1]
    if change_city:
        builder.button(
            text=await get_text_button("change_city"),
            callback_data=f"change_city_{form_type}",
        )
        tail.append(1)
    builder.button(
        text=await get_text_button("end_reg"), callback_data=f"end_reg_{form_type}"
    )
    builder.adjust(*adjust, *tail)
    return builder.as_markup()


async def rk_back_to_menu_form():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button("back_to_menu_form"))
    return builder.as_markup(resize_keyboard=True)