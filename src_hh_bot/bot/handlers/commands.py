from aiogram import Router
from aiogram.filters import Command, CommandObject, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import any_state
from aiogram.types import Message
from db import User
from sqlalchemy.ext.asyncio import AsyncSession
from tools import get_text_message

router = Router()


@router.message(Command(commands="reset"), StateFilter(any_state))
async def command_reset(
    message: Message,
    state: FSMContext,
    command: CommandObject,
    session: AsyncSession,
    user: User | None,
) -> None:
    await state.clear()
    await message.answer(text=await get_text_message("reset_done"))
