from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from bot.keyboards import Tag
from tools import get_num_column_for_tags, get_tags, get_text_button


async def ik_gen_tags_form_12():
    builder = InlineKeyboardBuilder()
    [builder.button(text=tag, callback_data=Tag(value=tag)) for tag in await get_tags()]
    builder.adjust(await get_num_column_for_tags())
    return builder.as_markup()


async def ik_gen_tags_form_34():
    builder = InlineKeyboardBuilder()
    [
        builder.button(text=tag, callback_data=Tag(value=tag))
        for tag in await get_tags(name_tags="tags_form_34")
    ]
    builder.adjust(
        await get_num_column_for_tags(name_column_tags="num_column_tags_form_34")
    )
    return builder.as_markup()


async def rk_gen_tags_form_12():
    builder = ReplyKeyboardBuilder()
    tags = await get_tags()

    for tag in tags:
        builder.button(text=tag)

    builder.button(text=await get_text_button("view_all_form"))
    builder.button(text=await get_text_button("cancel"))

    num_column = await get_num_column_for_tags()
    num_whole_tags, num_remaining_tags = divmod(len(tags), num_column)

    arr_tags = [num_column] * num_whole_tags
    if num_remaining_tags:
        arr_tags.append(num_remaining_tags)

    builder.adjust(*arr_tags, 2)
    return builder.as_markup(resize_keyboard=True)


async def rk_gen_tags_form_34():
    builder = ReplyKeyboardBuilder()
    tags = await get_tags(name_tags="tags_form_34")

    for tag in tags:
        builder.button(text=tag)

    builder.button(text=await get_text_button("view_all_form"))
    builder.button(text=await get_text_button("cancel"))

    num_column = await get_num_column_for_tags(
        name_column_tags="num_column_tags_form_34"
    )
    num_whole_tags, num_remaining_tags = divmod(len(tags), num_column)

    arr_tags = [num_column] * num_whole_tags
    if num_remaining_tags:
        arr_tags.append(num_remaining_tags)

    builder.adjust(*arr_tags, 2)
    return builder.as_markup(resize_keyboard=True)
