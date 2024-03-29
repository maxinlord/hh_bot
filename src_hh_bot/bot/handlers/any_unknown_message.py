from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from tools import get_text_message


router = Router()


@router.message(F.text == 'test')
async def test(
    message: Message
) -> None:
    pass


@router.message()
async def any_unknown_message(
    message: Message
) -> None:
    await message.answer(text=await get_text_message('answer_on_unknown_message'))


@router.callback_query()
async def any_unknown_callback(
        query: CallbackQuery) -> None:
    await query.message.edit_reply_markup(reply_markup=None)
