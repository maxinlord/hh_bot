from pprint import pprint
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.enums import MessageEntityType
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import User, Value
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
)
from bot.states import ViewForm
from bot.keyboards import (
    Form,
    Tag,
    k_form_fields,
    k_options_for_photo,
    k_gen_bttn_tags_inline,
    k_main_menu,
    k_back,
    k_view_form_menu,
    k_gen_bttn_tags_reply,
    k_back_reply,
    k_view_response,
)
from bot.filters import GetTextButton, FilterByTag


router = Router()


@router.message(GetTextButton("view_form"))
async def view_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("choose_a_tag"),
        reply_markup=await k_gen_bttn_tags_reply(),
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
    idpk_forms: list[int] = await get_idpk_forms(
        form_type=form_type_inverter[user.form_type],
        last_idpk_form=data.get("current_idpk", user.last_idpk_form),
    )
    if not idpk_forms:
        await message.answer(
            text=await get_text_message("no_forms"),
        )
        return
    form: User = await session.get(User, idpk_forms.pop(0))
    await state.update_data(idpk_forms=idpk_forms, current_idpk=form.idpk, tag=None)
    await message.answer(
        text=await get_text_message("search_forms"),
        reply_markup=await k_view_form_menu(),
    )
    await message.answer_media_group(
        media=ids_to_media_group(
            string_ids=form.field_5,
            caption=await get_text_message(
                "viewing_form",
                field_1=form.field_1,
                field_2=form.field_2,
                field_3=form.field_3,
            ),
        ),
    )
    await state.set_state(ViewForm.main)


@router.message(ViewForm.chose_tag, FilterByTag())
async def get_tag(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    tag = message.text
    data = await state.get_data()
    idpk_forms: list[int] = await get_idpk_forms_by_tag(
        tag=tag,
        form_type=form_type_inverter[user.form_type],
        last_idpk_form=data.get("current_idpk", user.last_idpk_form),
    )
    if not idpk_forms:
        await message.answer(
            text=await get_text_message("no_forms_with_tag", tag=tag),
        )
        return
    form: User = await session.get(User, idpk_forms.pop(0))
    await state.update_data(
        idpk_forms=idpk_forms,
        tag=tag,
        current_idpk=form.idpk,
    )
    await message.answer(
        text=await get_text_message("search_forms"),
        reply_markup=await k_view_form_menu(),
    )
    await message.answer_media_group(
        media=ids_to_media_group(
            string_ids=form.field_5,
            caption=await get_text_message(
                "viewing_form",
                field_1=form.field_1,
                field_2=form.field_2,
                field_3=form.field_3,
            ),
        ),
    )
    await state.set_state(ViewForm.main)


@router.message(ViewForm.main, GetTextButton("next"))
async def next_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    data = await state.get_data()
    idpk_forms: list[int] = data["idpk_forms"]
    if not idpk_forms:
        if data["tag"]:
            idpk_forms_updated = await get_idpk_forms_by_tag(
                tag=data["tag"],
                form_type=form_type_inverter[user.form_type],
                last_idpk_form=data["current_idpk"],
            )
        else:
            idpk_forms_updated = await get_idpk_forms(
                form_type=form_type_inverter[user.form_type],
                last_idpk_form=data["current_idpk"],
            )
        if not idpk_forms_updated:
            if data["tag"]:
                await message.answer(
                    text=await get_text_message("forms_with_tag_the_end"),
                )
            else:
                await message.answer(
                    text=await get_text_message("no_forms"),
                )
            return
        idpk_forms.extend(idpk_forms_updated)

    form: User = await session.get(User, idpk_forms.pop(0))
    await state.update_data(
        idpk_forms=idpk_forms,
        current_idpk=form.idpk,
    )
    await message.answer_media_group(
        media=ids_to_media_group(
            string_ids=form.field_5,
            caption=await get_text_message(
                "viewing_form",
                field_1=form.field_1,
                field_2=form.field_2,
                field_3=form.field_3,
            ),
        ),
    )
    await state.set_state(ViewForm.main)


@router.message(ViewForm.main, GetTextButton("end_viewing_form"))
async def end_viewing_form(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None:
    await message.answer(
        text=await get_text_message("main_menu"),
        reply_markup=await k_main_menu(),
    )
    data = await state.get_data()
    user.last_idpk_form = data["current_idpk"]
    await session.commit()
    await state.clear()


@router.message(ViewForm.main, GetTextButton("report"))
async def report(
    message: Message, state: FSMContext, session: AsyncSession, user: User
) -> None: ...


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
    MAX_SIZE_MESSAGE = 4096
    if len(message.text) > MAX_SIZE_MESSAGE:
        await message.answer(
            text=await get_text_message("mess_too_long"),
        )
        return
    await message.answer(
        text=await get_text_message("your_respond_send"),
        reply_markup=await k_view_form_menu(),
    )
    data = await state.get_data()
    responses: list = data.get("responses", [])
    responses.append(data["current_idpk"])
    await state.update_data(responses=responses)
    form = await session.get(User, data["current_idpk"])
    id_message = await save_message(message.text)
    await message.bot.send_message(
        chat_id=form.id_user,
        text=await get_text_message("you_have_response"),
        reply_markup=await k_view_response(id_message=id_message, idpk_form=user.idpk),
    )
    await state.set_state(ViewForm.main)
