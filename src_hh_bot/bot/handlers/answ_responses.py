from pprint import pprint
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums import MessageEntityType
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, Value, SendedMessage
from tools import (
    get_text_message,
    form_not_complete,
    get_idpk_forms_by_tag,
    get_idpk_forms,
    ids_to_media_group,
    ids_to_list,
    split_list_index,
    form_type_inverter,
    save_message,
    mention_html,
    delete_message,
)
from bot.states import ViewForm
from bot.keyboards import (
    Response,
    k_form_fields,
    k_options_for_photo,
    k_gen_bttn_tags_inline,
    k_main_menu,
    k_back,
    k_view_form_menu,
    k_gen_bttn_tags_reply,
    k_back_reply,
    k_view_response,
    k_accept_or_reject,
)
from bot.filters import GetTextButton, FilterByTag


router = Router()


@router.callback_query(Response.filter(F.type == "response"))
async def send_form_by_response(
    query: CallbackQuery,
    callback_data: Response,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    form: User = await session.get(User, callback_data.idpk_form)
    mess_response = await session.scalar(
        select(SendedMessage.message).where(
            SendedMessage.id_message == callback_data.id_message
        )
    )
    await delete_message(callback_data.id_message)
    await query.message.edit_reply_markup(reply_markup=None)
    if form.field_5:
        await query.message.answer_media_group(
            media=ids_to_media_group(
                string_ids=form.field_5,
                caption=await get_text_message(
                    "viewing_form",
                    field_1=form.field_1,
                    field_2=form.field_2,
                    field_3=form.field_3,
                ),
            )
        )
    else:
        await query.message.answer(
            text=await get_text_message(
                "viewing_form",
                field_1=form.field_1,
                field_2=form.field_2,
                field_3=form.field_3,
            ),
        )
    await query.message.answer(
        text=mess_response,
        reply_markup=await k_accept_or_reject(callback_data.idpk_form),
    )


@router.callback_query(F.data.startswith("response_accept"))
async def response_accept(
    query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    form = await session.get(User, query.data.split(":")[1])
    await query.bot.send_message(
        chat_id=user.id_user,
        text=await get_text_message(
            "response_accept",
            named_link=query.message.from_user.mention_html(
                name=await get_text_message("name_link_in_response")
            ),
        ),
    )
    await query.message.edit_reply_markup(reply_markup=None)
    await query.message.answer(
        text=await get_text_message(
            "response_accept_message",
            named_link=mention_html(
                id_user=form.id_user,
                name=await get_text_message("name_link_in_response"),
            ),
        )
    )


@router.callback_query(F.data == "response_reject")
async def response_reject(
    query: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    user: User,
) -> None:
    await query.message.edit_text(
        text=await get_text_message("response_reject_message")
    )
