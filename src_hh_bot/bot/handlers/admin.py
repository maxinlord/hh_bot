from pprint import pprint
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums import MessageEntityType
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, BlackList
from tools import get_text_message, form_not_complete
from bot.states import FormOneState
from bot.keyboards import (
    Form,
    Ban,
    Tag,
    k_form_fields,
    k_options_for_photo,
    k_gen_bttn_tags_inline,
    k_main_menu,
)
from bot.filters import GetTextButton


router = Router()


@router.callback_query(Ban.filter(F.type == "ban"))
async def answ_report(
    query: CallbackQuery,
    callback_data: Ban,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    user_to_ban = await session.get(User, callback_data.idpk_user)
    session.add(BlackList(id_user=user_to_ban.id_user))
    await session.commit()
    await query.message.edit_text(
        text=await get_text_message("user_banned", id_user=user_to_ban.id_user)
    )
