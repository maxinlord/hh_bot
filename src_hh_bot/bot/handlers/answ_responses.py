from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from bot.keyboards import (
    Response,
    k_accept_or_reject,
)
from db import SendedMessage, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tools import (
    delete_message,
    get_text_message,
    ids_to_media_group,
    mention_html,
    to_dict_form_fields,
)

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
    form_fields: dict = await to_dict_form_fields(form.form_fields)

    func = query.message.answer
    mess_data = {
        "text": await get_text_message(
            f"viewing_form_{user.form_type}",
            field_1=form_fields["field_1"],
            field_2=form_fields["field_2"],
            field_3=form_fields["field_3"],
            field_4=form_fields["field_4"],
            field_5=form_fields.get("field_5"),
            field_6=form_fields.get("field_6"),
        )
    }
    if form.form_type in ["one", "two"] and form_fields.get("field_5"):
        func = query.message.answer_media_group
        mess_data["media"] = ids_to_media_group(
            ids=form_fields["field_5"],
            caption=mess_data["text"],
        )
    await func(**mess_data)
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
    user_form_fields = await to_dict_form_fields(user.form_fields)
    await query.bot.send_message(
        chat_id=form.id_user,
        text=await get_text_message(
            "response_accept",
            field_1=user_form_fields["field_1"],
            field_2=user_form_fields["field_2"],
            field_3=user_form_fields["field_3"],
            named_link=mention_html(
                id_user=query.from_user.id,
                name=await get_text_message("name_link_in_response"),
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
