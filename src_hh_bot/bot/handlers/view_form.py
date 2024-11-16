import asyncio

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.filters import FilterByTag, GetTextButton
from bot.keyboards import (
    k_back_reply,
    k_ban,
    k_end_viewing_form,
    k_main_menu,
    k_view_form_menu,
    k_view_response,
    rk_gen_tags_form_12,
    rk_gen_tags_form_34,
)
from bot.states import ViewForm
from db import User
from sqlalchemy.ext.asyncio import AsyncSession
from tools import (
    form_type_inverter,
    get_city,
    get_forms_idpk,
    get_forms_idpk_by_tag,
    get_id_admin,
    get_text_message,
    ids_to_media_group,
    mention_html,
    save_message,
    save_viewing_form,
    to_dict_form_fields,
)

MAX_SIZE_MESSAGE = 4096
router = Router()


@router.message(GetTextButton("view_form"))
async def view_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if user.form_type in ["one", "two"]:
        await message.answer(
            text=await get_text_message("choose_a_tag"),
            reply_markup=await rk_gen_tags_form_12(),
        )
    elif user.form_type in ["three", "four"]:
        await message.answer(
            text=await get_text_message("choose_a_tag"),
            reply_markup=await rk_gen_tags_form_34(),
        )
    await state.set_state(ViewForm.chose_tag)


@router.message(ViewForm.chose_tag, GetTextButton("cancel"))
async def cancel_chose_tag(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("main_menu"),
        reply_markup=await k_main_menu(),
    )
    await state.clear()


@router.message(ViewForm.chose_tag, GetTextButton("view_all_form"))
async def view_all_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    city = await get_city(user.form_fields)
    forms_idpk: list[int] = await get_forms_idpk(
        form_type=form_type_inverter[user.form_type],
        last_form_idpk=data.get("current_idpk", user.last_idpk_form),
        city=city,
    )
    if not forms_idpk:
        await message.answer(
            text=await get_text_message("no_forms"),
        )
        return
    form: User = await session.get(User, forms_idpk.pop(0))
    form_fields = await to_dict_form_fields(form.form_fields)
    await state.update_data(forms_idpk=forms_idpk, current_idpk=form.idpk, tag=None)
    await message.answer(
        text=await get_text_message("search_forms"),
        reply_markup=await k_view_form_menu(),
    )
    await state.set_state(ViewForm.main)
    func = message.answer
    mess_data = {
        "text": await get_text_message(
            f"viewing_form_{user.form_type}",
            field_1=form_fields["field_1"],
            field_2=form_fields["field_2"],
            field_3=form_fields["field_3"],
            field_4=form_fields["field_4"],
            field_5=form_fields.get("field_5", None),
            field_6=form_fields.get("field_6", None),
        )
    }
    if user.form_type in ["one", "two"] and form_fields.get("field_5"):
        func = message.answer_media_group
        mess_data["media"] = ids_to_media_group(
            ids=form_fields["field_5"],
            caption=mess_data["text"],
        )
    await func(**mess_data)


@router.message(ViewForm.chose_tag, FilterByTag())
async def get_tag(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    tag = message.text
    data = await state.get_data()
    city = await get_city(user.form_fields)
    forms_idpk: list[int] = await get_forms_idpk_by_tag(
        tag=tag,
        form_type=form_type_inverter[user.form_type],
        last_form_idpk=data.get("current_idpk", user.last_idpk_form),
        city=city,
    )
    if not forms_idpk:
        await message.answer(
            text=await get_text_message("no_forms_with_tag", tag=tag),
        )
        return
    form: User = await session.get(User, forms_idpk.pop(0))
    form_fields = await to_dict_form_fields(form.form_fields)
    await state.update_data(
        forms_idpk=forms_idpk,
        tag=tag,
        current_idpk=form.idpk,
    )
    await message.answer(
        text=await get_text_message("search_forms"),
        reply_markup=await k_view_form_menu(),
    )
    await state.set_state(ViewForm.main)
    func = message.answer
    mess_data = {
        "text": await get_text_message(
            f"viewing_form_{user.form_type}",
            field_1=form_fields["field_1"],
            field_2=form_fields["field_2"],
            field_3=form_fields["field_3"],
            field_4=form_fields["field_4"],
            field_5=form_fields.get("field_5", None),
            field_6=form_fields.get("field_6", None),
        )
    }
    if user.form_type in ["one", "two"] and form_fields.get("field_5"):
        func = message.answer_media_group
        mess_data["media"] = ids_to_media_group(
            ids=form_fields["field_5"],
            caption=mess_data["text"],
        )
    await func(**mess_data)


async def update_forms_idpk(data, user):
    forms_idpk = data["forms_idpk"]
    if not forms_idpk:
        city = await get_city(user.form_fields)
        if data["tag"]:
            forms_idpk_updated = await get_forms_idpk_by_tag(
                tag=data["tag"],
                form_type=form_type_inverter[user.form_type],
                last_form_idpk=data["current_idpk"],
                city=city,
            )
        else:
            forms_idpk_updated = await get_forms_idpk(
                form_type=form_type_inverter[user.form_type],
                last_form_idpk=data["current_idpk"],
                city=city,
            )
        if not forms_idpk_updated:
            return None
        forms_idpk.extend(forms_idpk_updated)
    return forms_idpk


async def send_message(message, user, form_fields):
    text_message = await get_text_message(
        f"viewing_form_{user.form_type}",
        field_1=form_fields["field_1"],
        field_2=form_fields["field_2"],
        field_3=form_fields["field_3"],
        field_4=form_fields["field_4"],
        field_5=form_fields.get("field_5", None),
        field_6=form_fields.get("field_6", None),
    )
    func = (
        message.answer_media_group
        if user.form_type in ["one", "two"] and form_fields.get("field_5")
        else message.answer
    )
    mess_data = {"text": text_message}
    if func == message.answer_media_group:
        mess_data["media"] = ids_to_media_group(
            ids=form_fields["field_5"],
            caption=text_message,
        )
    await func(**mess_data)


@router.message(ViewForm.main, GetTextButton("next"))
async def next_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    forms_idpk = await update_forms_idpk(data, user)
    if not forms_idpk:
        await message.answer(
            text=await get_text_message(
                "forms_with_tag_the_end" if data["tag"] else "no_forms"
            ),
            reply_markup=await k_end_viewing_form(),
        )
        return
    form: User = await session.get(User, forms_idpk.pop(0))
    form_fields = await to_dict_form_fields(form.form_fields)
    await state.update_data(
        forms_idpk=forms_idpk,
        current_idpk=form.idpk,
    )
    await state.set_state(ViewForm.main)
    await send_message(message, user, form_fields)


@router.message(ViewForm.main, GetTextButton("end_viewing_form"))
async def end_viewing_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("main_menu"),
        reply_markup=await k_main_menu(),
    )
    await save_viewing_form(state=state, user=user, session=session)


@router.message(ViewForm.main, GetTextButton("report"))
async def report(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    if data["current_idpk"] in data.get("reports", []):
        await message.answer(
            text=await get_text_message("already_reported"),
        )
        return
    await message.answer(
        text=await get_text_message("send_me_reason_report"),
        reply_markup=await k_back_reply(),
    )
    await state.set_state(ViewForm.report)


@router.message(ViewForm.report, GetTextButton("back"))
async def back_to_viewing_menu(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("backed"),
        reply_markup=await k_view_form_menu(),
    )
    await state.set_state(ViewForm.main)


@router.message(ViewForm.report)
async def get_reason_report(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if len(message.text) > MAX_SIZE_MESSAGE:
        await message.answer(
            text=await get_text_message("mess_report_too_long"),
        )
        return

    # Fetch text messages and reply markup concurrently
    your_reason_send, view_form_menu = await asyncio.gather(
        get_text_message("your_reason_send"), k_view_form_menu()
    )
    await message.answer(
        text=your_reason_send,
        reply_markup=view_form_menu,
    )

    data = await state.get_data()
    reports = data.setdefault("reports", [])
    reports.append(data["current_idpk"])
    await state.update_data(reports=reports)

    form = await session.get(User, data["current_idpk"])
    form_fields = await to_dict_form_fields(form.form_fields)
    await state.set_state(ViewForm.main)

    # Fetch admin ID and text message concurrently
    id_admin, report_text = await asyncio.gather(
        get_id_admin(),
        get_text_message(
            f"report_form_{user.form_type}",
            field_1=form_fields["field_1"],
            field_2=form_fields["field_2"],
            field_3=form_fields["field_3"],
            field_4=form_fields["field_4"],
            field_5=form_fields.get("field_5", None),
            field_6=form_fields.get("field_6", None),
            reason=message.text,
            link_on_user=mention_html(
                form.id_user,
                form.name,
            ),
        ),
    )
    await message.bot.send_message(
        chat_id=id_admin,
        text=report_text,
        reply_markup=await k_ban(form.idpk),
    )


@router.message(ViewForm.main, GetTextButton("response"))
async def response(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    if data["current_idpk"] in data.get("responses", []):
        await message.answer(
            text=await get_text_message("already_response"),
        )
        return
    await message.answer(
        text=await get_text_message("send_me_message"),
        reply_markup=await k_back_reply(),
    )
    await state.set_state(ViewForm.response)


@router.message(ViewForm.response, GetTextButton("back"))
async def back_to_viewing_menu(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("backed"),
        reply_markup=await k_view_form_menu(),
    )
    await state.set_state(ViewForm.main)


@router.message(ViewForm.response)
async def get_mess_response(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    if len(message.text) > MAX_SIZE_MESSAGE:
        await message.answer(text=await get_text_message("mess_too_long"))
        return

    await message.answer(
        text=await get_text_message("your_respond_send"),
        reply_markup=await k_view_form_menu(),
    )

    data = await state.get_data()
    current_idpk = data["current_idpk"]
    responses = data.get("responses", [])
    responses.append(current_idpk)
    await state.update_data(responses=responses)

    form = await session.get(User, current_idpk)
    id_message = await save_message(message.text)

    await message.bot.send_message(
        chat_id=form.id_user,
        text=await get_text_message("you_have_response"),
        reply_markup=await k_view_response(id_message=id_message, idpk_form=user.idpk),
    )

    await state.set_state(ViewForm.main)
