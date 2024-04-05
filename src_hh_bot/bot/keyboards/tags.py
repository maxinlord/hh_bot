from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from tools import get_tags, get_num_column_for_tags, get_text_button
from bot.keyboards import Tag

async def k_gen_bttn_tags_inline():
    builder = InlineKeyboardBuilder()
    [
        builder.button(text=tag, callback_data=Tag(value=tag))
        for tag in await get_tags()
    ]
    builder.adjust(await get_num_column_for_tags())
    return builder.as_markup()


async def k_gen_bttn_tags_reply():
    builder = ReplyKeyboardBuilder()
    tags = await get_tags()
    [
        builder.button(text=tag)
        for tag in tags
    ]
    builder.button(text=await get_text_button('view_all_form'))
    builder.button(text=await get_text_button('cancel'))
    num_column = await get_num_column_for_tags()
    num_whole_string_tags = len(tags) // num_column
    num_remains_tags = len(tags) % num_column
    arr_tags = [num_column for _ in range(num_whole_string_tags)]
    if num_remains_tags:
        arr_tags.append(num_remains_tags)
    builder.adjust(*arr_tags, 2)
    return builder.as_markup(resize_keyboard=True)