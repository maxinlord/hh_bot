from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from tools import get_text_button


async def k_start_menu():
    builder = InlineKeyboardBuilder()
    builder.button(
        text=await get_text_button("registration"), callback_data="select_reg"
    )
    builder.button(
        text=await get_text_button("conditions_and_recommendations"),
        callback_data="pre_reg_info",
    )
    builder.adjust(1)
    return builder.as_markup()


async def k_main_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button("my_form"))
    builder.button(text=await get_text_button("view_form"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def k_my_form_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button("edit_my_form"))
    builder.button(text=await get_text_button("delete_my_form"))
    builder.button(text=await get_text_button("back"))
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)


async def k_view_form_menu():
    builder = ReplyKeyboardBuilder()
    builder.button(text=await get_text_button('estimate'))
    builder.button(text=await get_text_button('report'))
    builder.button(text=await get_text_button('next'))
    builder.button(text=await get_text_button('end_viewing_form'))
    builder.adjust(3, 1)
    return builder.as_markup(resize_keyboard=True)
