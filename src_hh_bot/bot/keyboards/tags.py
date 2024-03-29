from aiogram.utils.keyboard import InlineKeyboardBuilder
from tools import get_tags, get_num_column_for_tags 
from bot.keyboards import Tag

async def k_gen_bttn_tags():
    builder = InlineKeyboardBuilder()
    [
        builder.button(text=tag, callback_data=Tag(value=tag))
        for tag in await get_tags()
    ]
    builder.adjust(await get_num_column_for_tags())
    return builder.as_markup()
