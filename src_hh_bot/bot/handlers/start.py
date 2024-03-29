from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from db import User
from tools import get_text_message
from bot.keyboards import k_start_menu, k_types_of_reg, k_back


router = Router()


@router.message(CommandStart())
async def command_start(
    message: Message, state: FSMContext, command: CommandObject, session: AsyncSession, user: User | None
) -> None:
    await state.clear()
    await message.answer(text=await get_text_message("start", name_=message.from_user.full_name), reply_markup=await k_start_menu())


@router.callback_query(F.data == "select_reg")
async def process_select_reg(query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User) -> None:
    await query.message.edit_text(text=await get_text_message('select_type_registration'), reply_markup=await k_types_of_reg())

@router.callback_query(F.data == "pre_reg_info")
async def process_pre_reg_info(query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User) -> None:
    await query.message.edit_text(text=await get_text_message('pre_reg_info'), reply_markup=await k_back())


@router.callback_query(F.data == "back")
async def process_back(query: CallbackQuery, state: FSMContext, session: AsyncSession, user: User) -> None:
    await query.message.edit_text(text=await get_text_message('start', name_=query.from_user.full_name), reply_markup=await k_start_menu())
