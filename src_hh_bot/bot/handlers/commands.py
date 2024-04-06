from datetime import datetime
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
from tools import get_text_message
from bot.keyboards import k_start_menu, k_types_of_reg, k_back, k_main_menu
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

router = Router()


@router.message(CommandObject(command='reset'))
async def command_start(
    message: Message,
    state: FSMContext,
    command: CommandObject,
    session: AsyncSession,
    user: User | None,
) -> None:
    await state.clear()